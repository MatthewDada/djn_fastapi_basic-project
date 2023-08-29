from fastapi import FastAPI, HTTPException, status
from typing import Union, Optional 
from pydantic import BaseModel

app = FastAPI()

class Course(BaseModel):
    title: str 
    teacher: str
    students: Optional[list[str]] = []
    year : str


courses = {
    1: {
        "title": "Mechanics of Machines",
        "teacher": "Oyekeye",
        "students": ["Matthew", "Ademilade", "Saviour", "Olaolu"],
        "year": "300 level"
    },
    2: {
        "title": "Product Design",
        "teacher": "Orisaleye",
        "students": ["Matthew", "Ademilade", "Efezino", "Idris"],
        "year": "400 level"
    },
    3: {
        "title": "Statistics",
        "teacher": "Richard",
        "students": ["Matthew", "Malik", "Saviour", "Korede"],
        "year": "200 level"
    }
}


@app.get("/api/course/")
def get_all_courses(year: Union[str, None] = None):
    if year:
        year_course = []
        for index in courses.keys():
            if courses[index]["year"] == year:
                year_course.append(courses[index])
        return year_course   
    return courses


@app.get("/api/course/{course_id}/")
def deg_course(course_id: int):
    try:
        return courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code = 404, detail = f"Course with id:  {course_id} was not found!"
        )

    
@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    try:
        del courses[course_id] 
    except KeyError:
        raise HTTPException(
            status_code = 404, detail = f"Course with id:  {course_id} was not found!"
        )
    
@app.post("/api/courses", status_code=status.HTTP_204_NO_CONTENT)
def create_course(new_course: Course):
    course_id = max(courses.keys()) + 1
    courses[course_id] = new_course.model_dump()
    return courses[course_id]

@app.put("/api/courses/{course_id}")
def update_course(course_id: int, updated_courses: Course):
    try:
        course = courses[course_id]
        course["title"] = updated_courses.title
        course["teacher"] = updated_courses.teacher
        course["students"] = updated_courses.students
        course["year"] = updated_courses.year
    except KeyError:
        raise HTTPException(
            status_code = 404, detail = f"Course with id:  {course_id} was not found!"
        )
    