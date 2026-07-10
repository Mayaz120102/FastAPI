from fastapi import FastAPI, Path, HTTPException, Query, Body
import json

app = FastAPI()


def load_data():
    with open("students.json", "r") as f:
        data = json.load(f)

    return data


def save_data(data):
    with open("students.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return "student management system"


@app.get("/about")
def about():
    return "a fyulldf fsd flsfjsldf sdf"


@app.get("/view")
def view_student():
    data = load_data()
    return data


@app.get("/view/{student_id}")
def view_info(student_id: str = Path(..., description="student id", example="S001")):
    data = load_data()

    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail="student not found")


@app.get("/sort")
def view_sorted_by(
    sorted_by: str = Query(
        ..., description="sort on the basis of class, age , roll, marks"
    ),
    order: str = Query("asc", description="choose asc or desc"),
):

    valid_fields = [
        "age",
        "class",
        "roll",
        "Math marks",
        "English marks",
        "Science marks",
    ]
    if sorted_by not in valid_fields:
        raise HTTPException(
            status_code=404, detail=f"invalid input try with {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=404, detail="choose between asc or desc")

    data = load_data()

    sorted_order = True if order == "desc" else False

    sorted_data = list(data.values())

    sorted_data.sort(key=lambda x: x[sorted_by], reverse=sorted_order)

    return sorted_data


@app.post("/create")
def create_student(student: dict = Body()):

    data = load_data()

    student_id = student["id"]

    data[student_id] = student
    del data[student_id]["id"]
    save_data(data)

    return "Succesfully created student"
