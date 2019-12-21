from flask import Blueprint
auth = Blueprint('urls', __name__)
@auth.route('/sign_up',methods=['POST'])
def sign_up():
    return "user sign_up"