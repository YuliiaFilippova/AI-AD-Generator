from src.tts.generate_audio import generate_ad_audio
from src.video.mix_audio import create_video_with_ad
from src.video.audio_utils import extract_audio, create_combined_audio
from src.subtitles.subtitles_utils import convert_srt_to_vtt
import os
import shutil

print("📄 Converting subtitles to VTT...")
convert_srt_to_vtt(
    srt_path="data/output/output.srt",
    vtt_path="demo/subtitles.vtt"
)

print("Creating audiotrack with AD...")
generate_ad_audio("data/output/output.srt")

print("🎧 Extracting original audio...")
extract_audio(
    video_path="data/video/video.mp4",
    output_path="data/output/original_audio.wav"
)

print("🎧 Creating combined audio...")
create_combined_audio(
    original_audio="data/output/original_audio.wav",
    ad_audio="data/output/ad_track.wav",
    output_path="data/output/combined_audio.wav"
)


# for demo
print("Creating video with AD...")

# ensure folders exist
os.makedirs("data/output", exist_ok=True)
os.makedirs("demo", exist_ok=True)

main_output = "data/output/video_with_ad.mp4"
demo_output = "demo/video_with_ad.mp4"

# generate once
create_video_with_ad(
    video_path="data/video/video.mp4",
    ad_audio_path="data/output/ad_track.wav",
    output_path=main_output
)

# copy to demo
shutil.copy(main_output, demo_output)

print(f"Video saved to {main_output} and copied to {demo_output}")

print("Done.")