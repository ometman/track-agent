from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    parent_id: int

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    message: str
    to_user_id: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    from_user_id: int

    class Config:
        from_attributes = True

class ParentBase(BaseModel):
    name: str
    phone_number: str

class ParentCreate(ParentBase):
    pass

class Parent(ParentBase):
    id: int
    students: list[Student] = []

    class Config:
        from_attributes = True

class Notification(BaseModel):
    message: str

class GeofenceBase(BaseModel):
    name: str
    latitude: str
    longitude: str
    radius: int

class GeofenceCreate(GeofenceBase):
    pass

class Geofence(GeofenceBase):
    id: int

    class Config:
        from_attributes = True
