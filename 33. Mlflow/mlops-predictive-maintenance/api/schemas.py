from typing import Literal

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    type: Literal["L", "M", "H"]
    air_temperature_k: float = Field(ge=250, le=400)
    process_temperature_k: float = Field(ge=250, le=450)
    rotational_speed_rpm: float = Field(ge=0, le=30000)
    torque_nm: float = Field(ge=0, le=500)
    tool_wear_min: float = Field(ge=0, le=1000)


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    recommended_action: str
    model_version: str
