from fastapi import FastAPI, HTTPException, Path
import json

app = FastAPI()


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
def sortData(sort_by : str , order_by : str):
    if sort_by != 'age':
        raise HTTPException(status_code=400 , detail='wrong sort')
    
    orders = ['asc' , 'desc']
    if order_by not in orders:
        raise HTTPException(status_code=404 , detail="wrong")
    data = loadData()
    
    reverse_order = True if order_by == 'desc' else False
    
    if isinstance(data, dict):
        sorted_data = dict(sorted(data.items(), key=lambda item: item[1].get('age', 0), reverse=reverse_order))
    else:
        sorted_data = sorted(data, key=lambda x: x.get('age', 0), reverse=reverse_order)
    
    return {
        'data' : sorted_data
    }
    