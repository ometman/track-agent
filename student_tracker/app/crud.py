from sqlalchemy.orm import Session
from . import models, schemas
from .models import models as db_models

def get_parent(db: Session, parent_id: int):
    return db.query(db_models.Parent).filter(db_models.Parent.id == parent_id).first()

def get_parents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Parent).offset(skip).limit(limit).all()

def create_parent(db: Session, parent: schemas.ParentCreate):
    db_parent = db_models.Parent(name=parent.name, phone_number=parent.phone_number)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate, parent_id: int):
    db_student = db_models.Student(**student.model_dump(), parent_id=parent_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_geofence(db: Session, geofence_id: int):
    return db.query(db_models.Geofence).filter(db_models.Geofence.id == geofence_id).first()

def get_geofences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Geofence).offset(skip).limit(limit).all()

def create_geofence(db: Session, geofence: schemas.GeofenceCreate):
    db_geofence = db_models.Geofence(**geofence.model_dump())
    db.add(db_geofence)
    db.commit()
    db.refresh(db_geofence)
    return db_geofence

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Message).offset(skip).limit(limit).all()

def create_message(db: Session, message: schemas.MessageCreate, from_user_id: int):
    db_message = db_models.Message(**message.model_dump(), from_user_id=from_user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
