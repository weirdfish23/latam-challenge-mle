import fastapi
from fastapi import HTTPException
import pandas as pd
from challenge.model import DelayModel
from typing import List
from pydantic import BaseModel, ValidationError, validator


app = fastapi.FastAPI()

# initialize model at start up
delay_model = DelayModel()
data = pd.read_csv(filepath_or_buffer="data/data.csv")
app.valid_opera = data["OPERA"].unique().tolist()

x_train, y_train = delay_model.preprocess(data=data, target_column="delay")
delay_model.fit(x_train, y_train)
app.delay_model = delay_model


# /predict input body definition


class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

    @validator("OPERA")
    def validate_opera(opera):
        if opera not in app.valid_opera:
            raise HTTPException(status_code=400, detail=f"{opera} is not a valid OPERA")
        return opera

    @validator("TIPOVUELO")
    def validate_tipo_vuelo(tipo_vuelo):
        if tipo_vuelo not in ["N", "I"]:
            raise HTTPException(
                status_code=400, detail=f"{tipo_vuelo} is not a valid TIPOVUELO"
            )
        return tipo_vuelo

    @validator("MES")
    def validate_mes(mes):
        if mes < 1 or mes > 12:
            raise HTTPException(status_code=400, detail=f"{mes} is not a valid MES")
        return mes


class DelayPredictionInputBody(BaseModel):
    flights: List[Flight]


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.get("/", status_code=200)
async def root() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(data: DelayPredictionInputBody) -> dict:
    data = data.dict()
    raw_x = pd.DataFrame(data["flights"])
    x = app.delay_model.preprocess(raw_x)
    prediction = app.delay_model.predict(x)

    return {"predict": prediction}
