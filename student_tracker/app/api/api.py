from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..models import models
from ..database import SessionLocal
from ..services import notifications

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/parents/", response_model=schemas.Parent)
def create_parent(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    return crud.create_parent(db=db, parent=parent)

@router.get("/parents/", response_model=list[schemas.Parent])
def read_parents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parents = crud.get_parents(db, skip=skip, limit=limit)
    return parents

@router.get("/parents/{parent_id}", response_model=schemas.Parent)
def read_parent(parent_id: int, db: Session = Depends(get_db)):
    db_parent = crud.get_parent(db, parent_id=parent_id)
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@router.post("/parents/{parent_id}/students/", response_model=schemas.Student)
def create_student_for_parent(
    parent_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    return crud.create_student(db=db, student=student, parent_id=parent_id)

@router.get("/students/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.post("/notify/in-school/{student_id}")
def notify_in_school(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    parent = student.parent
    message = f"Your child, {student.name}, has arrived at school."
    notifications.send_notification(parent.phone_number, message)
    return {"message": "Notification sent successfully"}

@router.post("/notify/emergency/{student_id}")
def notify_emergency(student_id: int, notification: schemas.Notification, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    parent = student.parent
    notifications.send_notification(parent.phone_number, notification.message)
    return {"message": "Notification sent successfully"}

@router.post("/notify/picked-up/{student_id}")
def notify_picked_up(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    parent = student.parent
    message = f"Your child, {student.name}, has been picked up from school."
    notifications.send_notification(parent.phone_number, message)
    return {"message": "Notification sent successfully"}

@router.post("/geofences/", response_model=schemas.Geofence)
def create_geofence(geofence: schemas.GeofenceCreate, db: Session = Depends(get_db)):
    return crud.create_geofence(db=db, geofence=geofence)

@router.get("/geofences/", response_model=list[schemas.Geofence])
def read_geofences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    geofences = crud.get_geofences(db, skip=skip, limit=limit)
    return geofences

from ..services import geofencing

@router.get("/geofences/{geofence_id}", response_model=schemas.Geofence)
def read_geofence(geofence_id: int, db: Session = Depends(get_db)):
    db_geofence = crud.get_geofence(db, geofence_id=geofence_id)
    if db_geofence is None:
        raise HTTPException(status_code=404, detail="Geofence not found")
    return db_geofence

@router.post("/students/{student_id}/location")
def update_student_location(student_id: int, latitude: str, longitude: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.latitude = latitude
    student.longitude = longitude
    db.commit()
    geofences = crud.get_geofences(db)
    geofencing.check_geofence(student, geofences)
    return {"message": "Student location updated successfully"}

@router.post("/students/{student_id}/panic")
def panic(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    parent = student.parent
    message = f"EMERGENCY: {student.name} has pressed the panic button. Their location is {student.latitude}, {student.longitude}."
    notifications.send_notification(parent.phone_number, message)
    return {"message": "Panic signal sent successfully"}

@router.post("/messages/", response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db), current_user: models.Parent = Depends(get_db)):
    # This is a placeholder for getting the current user
    # In a real application, you would get the user from the request's authentication information
    from_user_id = 1
    return crud.create_message(db=db, message=message, from_user_id=from_user_id)

@router.get("/messages/", response_model=list[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages
