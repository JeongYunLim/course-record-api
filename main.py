from pathlib import Path
from typing import Literal
import json

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()

# main.py와 같은 폴더에 있는 courses.json 파일 경로
FILE_PATH = Path(__file__).parent / "courses.json"


# POST 요청으로 받을 수강기록 형식
class Course(BaseModel):
    course_name: str = Field(min_length=1, description="과목명")
    year: str = Field(pattern=r"^\d{4}$", description="4자리 이수연도")
    semester: Literal["1", "2"]
    grade: Literal["A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F"]


# courses.json 파일에서 전체 수강기록 읽기
def load_courses():
    if not FILE_PATH.exists():
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# 변경된 전체 수강기록을 courses.json 파일에 저장하기
def save_courses(courses):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)


# 서버 실행 확인용
@app.get("/")
def root():
    return {"message": "Course Record API is running"}


# 전체 수강기록 조회
@app.get("/courses")
def get_courses():
    courses = load_courses()
    return courses


# 새로운 수강기록 추가
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