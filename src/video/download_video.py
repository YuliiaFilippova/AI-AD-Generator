import os
import shutil
import yt_dlp


def download_video(url):
    # Main folder
    os.makedirs("data/video", exist_ok=True)
    os.makedirs("demo", exist_ok=True)

    path = "data/video/video.mp4"

    ydl_opts = {
        "outtmpl": path,
        "format": "mp4"
    }

    # Download once
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Copy to demo
    demo_path = "demo/video.mp4"
    shutil.copy(path, demo_path)

    print(f"Video saved to {path} and copied to {demo_path}")

    return path
