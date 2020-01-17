from db.database import Base,Engine
from auth.models import *
from patient.models import*
######## initDB  for creating the Table ##########
base = Base();
base.metadata.drop_all(Engine)
base.metadata.create_all(Engine)