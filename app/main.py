from fastapi import FastAPI,HTTPException,status,Response,Depends
from pydantic import BaseModel,HttpUrl
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from app import models,schemas
from sqlalchemy.orm import Session
from app.database import engine, get_db
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



while True:
       try:
              conn = psycopg2.connect(host = "localhost", port="5433", database ="aiquest", user = "postgres",password = "1234",
              cursor_factory = RealDictCursor)
              cursor = conn.cursor()
              print('successfully connected database')
              break
       except Exception as error:
              print('Databse conection failed')
              print("Error",error )
              time.sleep(2)

# @app.post("/post")
# def create_post(post:Course):
#        cursor.execute(""" INSERT INTO course(name,instructor, duration,website) VALUES (%s,%s,%s,%s) RETURNING *""", (post.name,post.
#        instructor, post.duration, str(post.website)))
#        new_post = cursor.fetchone()
#        conn.commit()
#        return {"Data": new_post}

# using sqlalchemi
@app.post("/courses", response_model=schemas.CourseResponse)
def create_course(course:schemas.CourseCreate, db :Session = Depends(get_db)):
       new_course = models.Course(** course.model_dump())
       new_course.website = str(course.website)
       db.add(new_course)
       db.commit()
       db.refresh(new_course)
       return new_course

# @app.get("/")
# def aiquest():
#     cursor.execute(""" SELECT * FROM course """)
#     data = cursor.fetchall()
#     return {"Data": data}

# using sqlalchemy
@app.get("/coursealchemy" , response_model=List[schemas.CourseResponse])
def course (db:Session = Depends(get_db)):
       course = db.query(models.Course).all()
       return course

# @app.get("/course")
# def studyMart():
#         return {"Course" : "Django and backend developement with python "}  

# @app.get("/django/api")
# def django():
#         return {"type" : "Basic to Advance"}

# @app.get("/course/{id}")
# def get_course(id:int):
#        cursor.execute("""SELECT * FROM course where id = %s """, (str(id),))
#        course = cursor.fetchone()
#        if not course:
#               raise HTTPException(
#                      status_code = status.HTTP_404_NOT_FOUND,
#                      detail = f"course with id:{id} was not found"
#               )
#        return{"course_details": course}

# using sqlalchemy
@app.get("/coursealchemy/{id}" , response_model=schemas.CourseResponse)
def my_course (id:int, db:Session = Depends(get_db)):
       course = db.query(models.Course).filter(models.Course.id == id).first()
       if not course:
              raise HTTPException(
                     status_code = status.HTTP_404_NOT_FOUND,
                     detail = f"course with id:{id} was not found"
              )
       return course


# using raw SQL
# @app.delete("/course/{id}" , status_code=status.HTTP_204_NO_CONTENT)
# def delete_course(id:int):
#        cursor.execute("""DELETE FROM course where id = %s returning *""", (str(id),))
#        delete_course = cursor.fetchone()
#        conn.commit()
#        if delete_course == None:
#               raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"course with id :{id} does not exist")
#        return Response(status_code=status.HTTP_204_NO_CONTENT)

# using sqlalchemy
@app.delete("/rafikul_course/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rafikul_course(id: int, db: Session = Depends(get_db)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"course with id:{id} was not found"
        )

    course_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# using raw sql
# @app.put("/course/{id}")
# def update_course(id: int, course: Course):

#     cursor.execute(
#         """ UPDATE course SET name = %s,
#             instructor = %s,
#             duration = %s,
#             website = %s
#         WHERE id = %s
#         RETURNING *;
#         """,
#         (course.name, course.instructor, course.duration, str(course.website), str(id))
#     )

#     updated_course = cursor.fetchone()
#     conn.commit()

#     if updated_course is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {id} does not exist"
#         )
#     return {"updated_course": updated_course}

# using aqlalchemy
@app.put("/rafikul_course/{id}" , response_model=schemas.CourseResponse)
def updated_rafikul_course (id:int, updated_course:schemas.CourseCreate , db:Session = Depends(get_db)):
       course_query = db.query(models.Course).filter(models.Course.id == id)
       course = course_query.first()
       if not course:
              raise HTTPException(
                     status_code = status.HTTP_404_NOT_FOUND,
                     detail = f"course with id:{id} was not found"
              )
       update_data = updated_course.model_dump()
       update_data ["website"] = str(update_data["website"])
       course_query.update(update_data,synchronize_session=False)
       db.commit()
       db.refresh(course)
       return course

       