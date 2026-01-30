
from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from app import models,schemas
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app import oauth2

router = APIRouter(prefix="/course",
                   tags=['Course'])


# using sqlalchemi
@router.post("/", response_model=schemas.CourseResponse)
def create_course(course:schemas.CourseCreate, db :Session = Depends(get_db), current_user :models.User = Depends(oauth2.get_current_user)):
       new_course = models.Course(** course.model_dump())
       new_course.website = str(course.website)
       db.add(new_course)
       db.commit()
       db.refresh(new_course)
       return new_course



# using sqlalchemy
@router.get("/" , response_model=List[schemas.CourseResponse])
def course (db:Session = Depends(get_db), current_user :models.User = Depends(oauth2.get_current_user)):
       course = db.query(models.Course).all()
       return course


# using sqlalchemy
@router.get("/{id}" , response_model=schemas.CourseResponse)
def my_course (id:int, db:Session = Depends(get_db) , current_user :models.User = Depends(oauth2.get_current_user)):
       course = db.query(models.Course).filter(models.Course.id == id).first()
       if not course:
              raise HTTPException(
                     status_code = status.HTTP_404_NOT_FOUND,
                     detail = f"course with id:{id} was not found"
              )
       return course

# using sqlalchemy
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rafikul_course(id: int, db: Session = Depends(get_db), current_user :models.User = Depends(oauth2.get_current_user)):
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

# using sqlalchemy
@router.put("/{id}" , response_model=schemas.CourseResponse)
def updated_rafikul_course (id:int, updated_course:schemas.CourseCreate , db:Session = Depends(get_db)
       , current_user :models.User = Depends(oauth2.get_current_user)):
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
