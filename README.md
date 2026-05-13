# 🎬 Automatic Audio Description for Short Videos

This project presents a lightweight pipeline for generating audio descriptions (AD) for short-form videos, aimed at improving accessibility for visually impaired viewers.
---

## Features

* Automatic video segmentation
* Keyframe extraction from scenes
* Visual understanding using VLMs
* Context-aware scene summarization using LLMs
* Subtitle (.srt) generation
* Text-to-speech generation with Piper
* Audio mixing with original video
* Lightweight demo web application
* Fully local pipeline (no cloud APIs required)

---

## System Overview

**Pipeline:**

```text
Video
  ↓
Scene Splitting
  ↓
Keyframe Extraction
  ↓
Vision-Language Model (Scene Descriptions)
  ↓
LLM Refinement + Context Tracking
  ↓
Subtitle Generation (.srt)
  ↓
Text-to-Speech (Piper)
  ↓
Audio Mixing
  ↓
Final Accessible Video
```

---

## Project Structure

```
AI-AD-Generator/

backend/        # backend logic / API (future expansion)
frontend/       # demo web application

models/         # Piper TTS models

src/
├── frames/     # keyframe extraction
├── llm/        # subtitle refinement / summarization
├── scenes/     # scene splitting
├── subtitles/  # SRT generation
├── tts/        # Piper integration
├── utils/      # helper utilities
├── video/      # video/audio processing
└── vlm/        # vision-language scene description

generate_pipeline.py   # main pipeline
requirements.txt
README.md
```

---

## Models Used

* VLM: Qwen2-VL-2B-Instruct (optional stronger model: Qwen/Qwen2-VL-7B-Instruct)
* LLM: qwen2.5:14b (optional stronger models: qwen2.5:32b or qwen2.5:72b)
* TTS: Piper

---

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Make sure you have Ollama installed and running.

Pull the required models:

```bash
ollama pull qwen2.5:14b
```

Install ffmpeg (required for audio/video processing):

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt install ffmpeg
```

**Windows:**
Download from: https://ffmpeg.org/download.html
and add it to your system PATH.

## Models

This project uses a local TTS model from Piper.

Download the required model manually from Hugging Face:

https://huggingface.co/rhasspy/piper-voices

Example model used in this project:

* en_GB-alba-medium.onnx
* en_GB-alba-medium.onnx.json

Place the downloaded files in the `models/` directory:

```
models/
  en_GB-alba-medium.onnx
  en_GB-alba-medium.onnx.json
```


---

## Demo Web Application

The web application has two parts:

- Backend: FastAPI server
- Frontend: React/Vite interface

### 1. Start the backend
From the project root:

```bash
python -m uvicorn backend.app.main:app --reload
```

The backend will run locally, usually at:
[http://127.0.0.1:8000
](http://127.0.0.1:8000)

### 2. Start the frontend
Open a second terminal, then run:

```bash
cd frontend
npm run dev
```
The frontend will run locally, usually at:

[http://localhost:5173
](http://localhost:5173)

Open the frontend URL in your browser and upload a video to run the audio-description pipeline.

---

## Evaluation

The system can be evaluated based on:

* Descriptiveness
* Objectivity
* Accuracy
* Clarity
* Optional qualitative feedback

---

## Limitations

* Visual model may miss details or produce imperfect descriptions
* Descriptions may sometimes be overly simple
* Processing is not real-time

---

## Future Work

* Better scene boundary detection
* Multi-character tracking
* Improved temporal consistency
* Placing web application on a server
* Multi-audio track support in video player with multi-language narration
* Evaluation with users

---

## Author

Yuliia Filippova


