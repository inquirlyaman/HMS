from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

#patient models
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique = True)
    mobile = Column(String(255))
    address = Column(String(255) )
    sex = Column(String(15))
    age = Column(String(3))
    blood_group = Column(String(10))
    
    def __init__(self, name, email,mobile,address,sex,age,blood_group):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.address = address
        self.sex = sex
        self.age = age
        self.blood_group = blood_group