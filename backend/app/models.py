from pydantic import BaseModel


# ----------------------------
# YOUTUBE GENERATION REQUEST
# ----------------------------

class YouTubeRequest(BaseModel):
    url: str
    participant_id: str


# ----------------------------
# EVALUATION REQUEST
# ----------------------------

class EvaluationRequest(BaseModel):
    job_id: str

    descriptiveness: int
    objectivity: int
    accuracy: int
    clarity: int

    feedback: str = ""