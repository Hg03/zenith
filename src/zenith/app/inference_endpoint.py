from zenith.pipelines.inference_pipeline import InferencePipeline
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, status
import uvicorn

app = FastAPI()


class PredictionInput(BaseModel):
    person_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=10, le=100)
    daily_screen_time_min: int = Field(..., ge=0, le=1440)
    platform: str
    social_media_time_min: int = Field(..., ge=0, le=1440)
    negative_interactions_count: int = Field(..., ge=0)
    positive_interactions_count: int = Field(..., ge=0)
    sleep_hours: int = Field(..., ge=0, le=24)
    physical_activity_min: int = Field(..., ge=0, le=1440)
    anxiety_level: int = Field(..., ge=0, le=10)
    gender: str

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        allowed = {"Male", "Female", "Other"}
        if v not in allowed:
            raise ValueError(f"gender must be one of {allowed}")
        return v

    @field_validator("platform")
    @classmethod
    def validate_platform(cls, v):
        allowed = {"Facebook", "Instagram", "Snapchat", "TikTok"}
        if v not in allowed:
            raise ValueError(f"platform must be one of {allowed}")
        return v


class ResponseModel(BaseModel):
    mental_state: str


@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "zenith"}


@app.post("/predict", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def prediction_service(input: PredictionInput):
    infer_runner = InferencePipeline()
    features = input.model_dump()
    result = infer_runner.execute(PredictionInput=features)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="8000")
