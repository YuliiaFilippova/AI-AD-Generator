import srt
import wave
import os
from pathlib import Path
from datetime import timedelta
from piper import PiperVoice
import subprocess

ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = ROOT_DIR / "models" / "en_GB-alba-medium.onnx"
CONFIG_PATH = ROOT_DIR / "models" / "en_GB-alba-medium.onnx.json"

GLOBAL_OFFSET = 2.0   # delay at start (seconds)
AD_VOLUME = 6.0       # boost AD loudness

def time_to_seconds(t: timedelta):
    return t.total_seconds()

def generate_ad_audio(srt_path, output_path):
    # Load subtitles
    with open(srt_path, "r") as f:
        subtitles = list(srt.parse(f.read()))

    # Load Piper model
    voice = PiperVoice.load(MODEL_PATH, config_path=CONFIG_PATH)

    output_path = Path(output_path)
    temp_dir = output_path.parent / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    #temp_dir = Path("data/output/temp")
    #temp_dir.mkdir(parents=True, exist_ok=True)

    wav_files = []

    print("Generating speech...")

    current_time = 0.0  # prevent overlap

    # Step 1: generate wav files
    for i, sub in enumerate(subtitles):
        text = sub.content.replace("\n", " ")
        start_time = time_to_seconds(sub.start)

        temp_file = temp_dir / f"line_{i}.wav"

        with wave.open(str(temp_file), "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)

        # get duration
        with wave.open(str(temp_file), "rb") as wf:
            duration = wf.getnframes() / wf.getframerate()

        # prevent overlap + add global delay
        actual_start = max(start_time, current_time)
        actual_start += GLOBAL_OFFSET

        wav_files.append((temp_file, actual_start))

        current_time = actual_start + duration + 0.2  # small gap

    print("Building timeline...")

    inputs = []
    filters = []

    for i, (file, start) in enumerate(wav_files):
        inputs.extend(["-i", str(file)])

        delay = int(start * 1000)

        # 🔊 volume boost per segment
        filters.append(f"[{i}:a]volume={AD_VOLUME},adelay={delay}|{delay}[a{i}]")

    mix_inputs = "".join([f"[a{i}]" for i in range(len(wav_files))])

    filter_complex = (
        ";".join(filters)
        + f";{mix_inputs}amix=inputs={len(wav_files)}:duration=longest"
    )

    print("Rendering final audio...")

    cmd = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_complex,
        "-y",
        output_path
    ]

    subprocess.run(cmd, check=True)

    print(f"✅ Audio description saved to {output_path}")