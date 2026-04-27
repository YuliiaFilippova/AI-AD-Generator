import subprocess

def create_video_with_ad(video_path, ad_audio_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", ad_audio_path,
        "-filter_complex",
        "[0:a]volume=0.2[a0];[a0][1:a]amix=inputs=2:duration=longest",
        "-c:v", "copy",
        "-y",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"Final video saved to {output_path}")