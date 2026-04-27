import subprocess


def extract_audio(video_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0",
        "-map", "a",
        "-y",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"Original audio saved to {output_path}")


def create_combined_audio(original_audio, ad_audio, output_path):
    cmd = [
        "ffmpeg",
        "-i", original_audio,
        "-i", ad_audio,
        "-filter_complex",
        "[0:a]volume=0.4[a0];[1:a]volume=2.0[a1];[a0][a1]amix=inputs=2:duration=longest",
        "-y",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"Combined audio saved to {output_path}")