from flask import Flask
from auth.routes import auth
from patient.routes import patient
app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(patient)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
if __name__ == '__main__':
    app.run( port=5000, debug=True)