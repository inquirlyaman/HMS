from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique = True)
    password = Column(String(255), nullable= False)
    confirm_password = Column(String(255),nullable= False)
    
    def __init__(self,name,email,password,confirm_password):
        self.name = name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable = False)
    
    def __init__(self,name):
        self.name = name 
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer,ForeignKey('roles.id'))
    
    def __init__(self,user_id,role_id):
        self.user_id = user_id
        self.role_id = role_id