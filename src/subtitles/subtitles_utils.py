import subprocess

def convert_srt_to_vtt(srt_path, vtt_path):
    cmd = [
        "ffmpeg",
        "-i", srt_path,
        vtt_path,
        "-y"
    ]

    subprocess.run(cmd, check=True)
    print(f"Subtitles converted to {vtt_path}")