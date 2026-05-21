from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

FILE_NAME = "courses.json"


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def load_courses():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_courses(courses):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


@app.get("/")
def root():
    return {"message": "Course Record API is running"}


@app.get("/courses")
def get_courses():
    courses = load_courses()
    return courses


@app.post("/courses")
def add_course(course: Course):
    courses = load_courses()

    new_course = {
        "course_name": course.course_name,
        "year": course.year,
        "semester": course.semester,
        "grade": course.grade
    }

    courses.append(new_course)
    save_courses(courses)

    return {
        "message": "수강기록이 추가되었습니다.",
        "added_course": new_course,
        "total_count": len(courses)
    }