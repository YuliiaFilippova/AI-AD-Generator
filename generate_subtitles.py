from src.video.download_video import download_video
from src.scenes.detect_scenes import detect_scenes
from src.frames.extract_keyframes import extract_keyframes
from src.scenes.merge_short_scenes import merge_short_scenes

from src.vlm.llava_describe import describe_frame
from src.llm.summarize_scene import summarize_scene

from src.utils.timing import max_words
from src.subtitles.create_srt import create_srt

import shutil
import os

video_url = "https://www.youtube.com/watch?v=dxKPCPMaWFg"
shutil.rmtree("data/frames", ignore_errors=True)

print("Downloading video...")
video = download_video(video_url)

print("Detecting scenes...")
scenes = detect_scenes(video)

print("Merging short scenes...")

scenes = merge_short_scenes(scenes)

# for test to see new duration of the scene
print("Scenes after merging:")

for s in scenes:
    print(f"{s[0]:.2f} → {s[1]:.2f}  ({s[1]-s[0]:.2f}s)")

# for test
#scenes = scenes[:5]



print("Extracting keyframes...")
scene_frames = extract_keyframes(video, scenes)

descriptions = []
previous_summary = ""

print("Generating audio descriptions...")

for i, frames in enumerate(scene_frames):

    print(f"Scene {i+1}/{len(scene_frames)}")

    frame_descriptions = []

    for frame in frames:
        d = describe_frame(frame)
        frame_descriptions.append(d)

    words = max_words(scenes[i][0], scenes[i][1])

    narration = summarize_scene(frame_descriptions, previous_summary, words)

    # for testing
    print("Frame descriptions:")
    for d in frame_descriptions:
        print("-", d)

    print("Final narration:", narration)

    descriptions.append(narration)
    previous_summary = narration

print("Creating subtitles...")
create_srt(scenes, descriptions)