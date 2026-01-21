from fastapi import FastAPI
from pydantic import BaseModel,HttpUrl
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# define request body schema
class Course(BaseModel):
       name: str
       instructor: str
       duration:float
       website: HttpUrl

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

@app.post("/post")
def create_post(post:Course):
       cursor.execute(""" INSERT INTO course(name,instructor, duration,website) VALUES (%s,%s,%s,%s) RETURNING *""", (post.name,post.
       instructor, post.duration, str(post.website)))
       new_post = cursor.fetchone()
       conn.commit()
       return {"Data": new_post}

@app.get("/")
def aiquest():
    cursor.execute(""" SELECT * FROM course """)
    data = cursor.fetchall()
    return {"Data": data}

@app.get("/course")
def studyMart():
        return {"Course" : "Django and backend developement with python "}
    
@app.get("/django/api")
def django():
        return {"type" : "Basic to Advance"}