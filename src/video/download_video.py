import os
import shutil
import yt_dlp


def download_video(url, output_path):

    # create parent directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Video saved to {output_path}")

    return output_path
