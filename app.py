from flask import Flask
from auth.routes import auth
app = Flask(__name__)
app.register_blueprint(auth)


if __name__ == '__main__':
    app.run( port=5000, debug=True)