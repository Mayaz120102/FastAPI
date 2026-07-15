from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated, Optional
import json
from fastapi.responses import JSONResponse

app = FastAPI()


class Student(BaseModel):
    id: Annotated[str, Field(..., description="student id", example="S001")]
    name: Annotated[str, Field(..., description="student name")]
    age: Annotated[int, Field(..., gt=5, lt=18, description="age")]
    student_class: Annotated[int, Field(..., gt=1, lt=13, description="class")]
    roll: Annotated[int, Field(..., gt=0, lt=101, description="roll")]
    Math_marks: Annotated[int, Field(..., gt=0, lt=101)]
    English_marks: Annotated[int, Field(..., gt=0, lt=101)]
    Science_marks: Annotated[int, Field(..., gt=0, lt=101)]
    phone: Annotated[str, Field(..., example="01XXXXXXXX")]


class StudentUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[str], Field(default=None)]
    student_class: Annotated[Optional[int], Field(default=None)]
    roll: Annotated[Optional[int], Field(default=None)]
    Math_marks: Annotated[Optional[int], Field(default=None)]
    English_marks: Annotated[Optional[int], Field(default=None)]
    Science_marks: Annotated[Optional[int], Field(default=None)]
    phone: Annotated[Optional[int], Field(default=None)]


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
        ..., description="sort on the basis of student_class, age , roll, marks"
    ),
    order: str = Query("asc", description="choose asc or desc"),
):

    valid_fields = [
        "age",
        "student_class",
        "roll",
        "Math_marks",
        "English_marks",
        "Science_marks",
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
def create_student(student: Student):

    data = load_data()

    if student.id in data:
        raise HTTPException(status_code=400, detail="Student already exists")

    data[student.id] = student.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(
        status_code=201, content={"message": "Student Created Successfully"}
    )


@app.put("/edit/{student_id}")
def update_student(student_id: str, student: StudentUpdate):

    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")

    data[student_id].update(student.model_dump(exclude_unset=True))

    save_data(data)

    return JSONResponse(
        status_code=200, content={"message": "Student Updated Successfully"}
    )


@app.delete("/delete/{student_id}")
def delete_student(student_id: str):

    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")

    del data[student_id]

    save_data(data)

    return JSONResponse(
        status_code=200, content={"message": "Student Deleted Successfully"}
    )
