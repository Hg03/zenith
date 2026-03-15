from zenith.pipelines.inference_pipeline import InferencePipeline
from pydantic import BaseModel, Field
from fastapi import FastAPI, status
from enum import Enum
import uvicorn

app = FastAPI(title="Zenith Mental Health Prediction API", version="1.0.0")

infer_runner = InferencePipeline()


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class Platform(str, Enum):
    Facebook = "Facebook"
    Instagram = "Instagram"
    Snapchat = "Snapchat"
    TikTok = "TikTok"


class PredictionInput(BaseModel):
    person_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=10, le=100)
    daily_screen_time_min: int = Field(..., ge=0, le=1440)
    platform: Platform
    social_media_time_min: int = Field(..., ge=0, le=1440)
    negative_interactions_count: int = Field(..., ge=0)
    positive_interactions_count: int = Field(..., ge=0)
    sleep_hours: int = Field(..., ge=0, le=24)
    physical_activity_min: int = Field(..., ge=0, le=1440)
    anxiety_level: int = Field(..., ge=0, le=10)
    gender: Gender


class ResponseModel(BaseModel):
    mental_state: str


@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "zenith"}


@app.post("/predict", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def prediction_service(payload: PredictionInput):
    features = payload.model_dump()
    result = infer_runner.execute(PredictionInput=features)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
