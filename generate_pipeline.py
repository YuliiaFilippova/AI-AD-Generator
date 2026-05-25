import sys
import os
import json
import shutil
from uuid import uuid4
from difflib import SequenceMatcher

PROJECT_ROOT = os.path.abspath(
    os.path.dirname(__file__)
)

sys.path.insert(0, PROJECT_ROOT)

from src.video.download_video import download_video
from src.scenes.detect_scenes import split_by_time
from src.frames.extract_keyframes import extract_keyframes
from src.vlm.gwen_describe import describe_scene
from src.utils.similarity import are_similar
from src.llm.summarize_scene import generate_subtitle
from src.utils.timing import max_words
from src.subtitles.create_srt import create_srt

from src.tts.generate_audio import generate_ad_audio
from src.video.mix_audio import create_video_with_ad
from src.video.audio_utils import extract_audio, create_combined_audio
from src.subtitles.subtitles_utils import convert_srt_to_vtt



def similar(a, b):
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()



def run_pipeline(input_source, participant_id, is_youtube=False):

    job_id = str(uuid4())

    job_dir = f"backend/app/jobs/{job_id}"
    os.makedirs(job_dir, exist_ok=True)

    video_dir = os.path.join(job_dir, "video")
    output_dir = os.path.join(job_dir, "output")
    frames_dir = os.path.join(job_dir, "frames")

    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)

    video_path = os.path.join(video_dir, "input.mp4")

    # ---------------------------------
    # GET VIDEO
    # ---------------------------------

    if is_youtube:
        print("Downloading YouTube video...")

        download_video(
            input_source,
            video_path
        )

    else:
        shutil.copy(
            input_source,
            video_path
        )

    # ---------------------------------
    # DETECT SCENES
    # ---------------------------------

    print("Detecting scenes...")
    scenes = split_by_time(video_path, chunk_duration=8.0)

    # ---------------------------------
    # EXTRACT KEYFRAMES
    # ---------------------------------

    print("Extracting keyframes...")
    scene_frames = extract_keyframes(video_path, scenes, output_dir=frames_dir)

    # ---------------------------------
    # VLM DESCRIPTIONS
    # ---------------------------------

    print("Generating VLM descriptions...")

    vlm_descriptions = []

    for i, frames in enumerate(scene_frames):

        print(f"Scene {i+1}/{len(scene_frames)}")

        scene_description = describe_scene(frames)

        print(scene_description)

        vlm_descriptions.append(scene_description)


    # ---------------------------------
    # LLM REFINEMENT
    # ---------------------------------

    print("Refining descriptions with LLM...")

    final_descriptions = []
    previous_subtitles = []
    results = []

    for i, scene_description in enumerate(vlm_descriptions):

        words = max_words(scenes[i][0], scenes[i][1])

        history = [s for s in previous_subtitles if s.strip()]
        history = history[-2:]

        past = 1
        start = max(0, i - past)
        end = i

        local_context = "\n".join(
            f"Previous scene {j + 1}: {vlm_descriptions[j]}"
            for j in range(start, end)
        )

        narration = generate_subtitle(
            current_description=scene_description,
            previous_subtitles=history,
            max_words=words,
            local_context=local_context,
        )

        narration = narration.strip()

        if narration == "":
            continue
        # semantic similarity check
        # compare with previously KEPT subtitle, not just previous chunk
        if previous_subtitles:
            last_kept = previous_subtitles[-1]

            if are_similar(narration, last_kept, threshold=0.70):
                print(f"Skipped similar subtitle at scene {i + 1}")
                continue

        print("LLM:", narration)
        #print("HISTORY:", history)
        print("LOCAL COTEXT", local_context)
        print("-" * 40)

        previous_subtitles.append(narration)
        final_descriptions.append(narration)

    # ---------------------------------
    # CREATE SRT
    # ---------------------------------

    srt_path = os.path.join(output_dir, "output.srt")

    create_srt(scenes, final_descriptions, output_path=srt_path)

    # ---------------------------------
    # CONVERT TO VTT
    # ---------------------------------

    vtt_path = os.path.join(output_dir, "output.vtt")

    convert_srt_to_vtt(
        srt_path=srt_path,
        vtt_path=vtt_path
    )

    # ---------------------------------
    # GENERATE AD AUDIO
    # ---------------------------------

    print("Generating narration audio...")

    ad_audio_path = os.path.join(output_dir, "ad_track.wav")

    generate_ad_audio(
        srt_path=srt_path,
        output_path=ad_audio_path
    )

    # ---------------------------------
    # EXTRACT ORIGINAL AUDIO
    # ---------------------------------

    original_audio_path = os.path.join(output_dir, "original_audio.wav")

    extract_audio(
        video_path=video_path,
        output_path=original_audio_path
    )

    # ---------------------------------
    # COMBINE AUDIO
    # ---------------------------------

    combined_audio_path = os.path.join(output_dir, "combined_audio.wav")

    create_combined_audio(
        original_audio=original_audio_path,
        ad_audio=ad_audio_path,
        output_path=combined_audio_path
    )

    # ---------------------------------
    # CREATE FINAL VIDEO
    # ---------------------------------

    final_video_path = os.path.join(output_dir, "video_with_ad.mp4")

    create_video_with_ad(
        video_path=video_path,
        ad_audio_path=ad_audio_path,
        output_path=final_video_path
    )

    # ----------------------------
    # SAVE GENERATION METADATA
    # ----------------------------

    generation_data = {
        "job_id": job_id,
        "input_source": input_source,
        "participant_id": participant_id,

        "outputs": {
            "video_url": f"/jobs/{job_id}/output/video_with_ad.mp4",
            "audio_url": f"/jobs/{job_id}/output/combined_audio.wav",
            "srt_url": f"/jobs/{job_id}/output/output.srt",
            "vtt_url": f"/jobs/{job_id}/output/output.vtt"
        }
    }

    json_path = os.path.join(job_dir, "generation.json")

    with open(json_path, "w") as f:
        json.dump(generation_data, f, indent=2)

    return {
        "job_id": job_id,

        "video_url":
            f"/jobs/{job_id}/output/video_with_ad.mp4",

        "audio_url":
            f"/jobs/{job_id}/output/combined_audio.wav",

        "srt_url":
            f"/jobs/{job_id}/output/output.srt",

        "vtt_url":
            f"/jobs/{job_id}/output/output.vtt",

        "json_url":
            f"/jobs/{job_id}/generation.json"
    }
