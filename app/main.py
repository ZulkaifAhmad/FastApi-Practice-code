from fastapi import FastAPI, HTTPException, Path
import json
from pydantic import BaseModel, Field
from typing import Annotated, Literal

app = FastAPI()

from typing import Annotated, Literal
from pydantic import BaseModel, Field


class Patient(BaseModel):
    id: Annotated[int, Field(..., description="id is required and must be unique")]

    name: Annotated[
        str, Field(..., description="name is required", min_length=4, max_length=10)
    ]

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            lt=120,
            description="age must be greater than 0 and less than 120",
        ),
    ]

    gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="must be male, female or other"),
    ]

    disease: str = Field(..., description="must be a string and is required")

    admitted: Annotated[bool, Field(..., description="must be true or false")]


def loadData():
    with open("patient.json", "r") as file:
        data = json.load(file)
    return data


@app.get("/view")
def view():
    data = loadData()
    return {"message": "Loaded Successfully", "data": data}


@app.get("/patient/{id}")
def getPatient(id: str = Path(..., description="get patient data by id", example="1")):
    data = loadData()
    if id in data:
        return {"message": "Patient data loaded successfully", "data": data[id]}
    raise HTTPException(status_code=404, detail="patient not found")


@app.get("/sort")
def sortData(sort_by: str, order_by: str):
    if sort_by != "age":
        raise HTTPException(status_code=400, detail="wrong sort")

    orders = ["asc", "desc"]
    if order_by not in orders:
        raise HTTPException(status_code=404, detail="wrong")
    data = loadData()

    reverse_order = True if order_by == "desc" else False

    if isinstance(data, dict):
        sorted_data = dict(
            sorted(
                data.items(),
                key=lambda item: item[1].get("age", 0),
                reverse=reverse_order,
            )
        )
    else:
        sorted_data = sorted(data, key=lambda x: x.get("age", 0), reverse=reverse_order)

    return {"data": sorted_data}


@app.post("/create")
def create(payload: Patient):
    data = loadData()

    for patient in data:
        if patient["id"] == payload.id:
            raise HTTPException(
                status_code=400,
                detail="Patient already exists"
            )

    data.append(payload.model_dump())

    # Save updated data
    with open("patient.json", "w") as file:
        json.dump(data, file, indent=4)

    return {
        "message": "Patient created successfully",
        "data": payload
    }