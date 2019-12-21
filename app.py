from flask import Flask
from auth.routes import auth
from db.database import Base,Engine
from auth.models import *

######## initDB  for creating the Table ##########
base = Base();
base.metadata.drop_all(Engine)
base.metadata.create_all(Engine)
app = Flask(__name__)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run( port=5000, debug=True)