import sys
import os
import json
import uuid

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models import EvaluationRequest
from generate_pipeline import run_pipeline

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

JOBS_DIR = BASE_DIR / "jobs"

JOBS_DIR.mkdir(exist_ok=True)

app.mount(
    "/jobs",
    StaticFiles(directory=str(JOBS_DIR)),
    name="jobs"
)
#app.mount("backend/app/jobs", StaticFiles(directory="jobs"), name="jobs")
#os.makedirs("jobs", exist_ok=True)
#app.mount("/backend/app/jobs", StaticFiles(directory="jobs"), name="jobs")
#app.mount("/jobs", StaticFiles(directory="jobs"), name="jobs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class YoutubeRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {"message": "Audio Description API Running"}


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    upload_path = f"uploads/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = run_pipeline(upload_path)

    return results


@app.post("/youtube")
def youtube_video(request: YoutubeRequest):

    participant_id = str(uuid.uuid4())
    results = run_pipeline(
        request.url,
        participant_id=participant_id,
        is_youtube=True
    )

    return results

@app.get("/download/video/{job_id}")
def download_video(job_id: str):

    path = (BASE_DIR/"jobs"/job_id/"output"/"video_with_ad.mp4")

    return FileResponse(
        path=str(path),
        media_type="video/mp4",
        filename="video_with_ad.mp4"
    )

@app.get("/download/audio/{job_id}")
def download_audio(job_id: str):

    path = (BASE_DIR/"jobs"/job_id/"output"/"combined_audio.wav")

    return FileResponse(
        path=str(path),
        media_type="audio/wav",
        filename="combined_audio.wav"
    )


@app.get("/download/srt/{job_id}")
def download_srt(job_id: str):

    path = (BASE_DIR/"jobs"/job_id/"output"/"output.srt")

    return FileResponse(
        path=str(path),
        media_type="text/plain",
        filename="output.srt"
    )

@app.post("/evaluate")
def evaluate(data: EvaluationRequest):

    evaluations_path = "backend/app/evaluations.json"

    # create file if missing
    if not os.path.exists(evaluations_path):
        with open(evaluations_path, "w") as f:
            json.dump([], f)

    # load existing evaluations
    with open(evaluations_path, "r") as f:
        evaluations = json.load(f)

    # append new evaluation
    evaluations.append(data.dict())

    # save back
    with open(evaluations_path, "w") as f:
        json.dump(evaluations, f, indent=2)

    return {
        "status": "success"
    }