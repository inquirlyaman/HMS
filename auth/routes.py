from flask import Blueprint, request, jsonify
auth = Blueprint('urls', __name__)
from auth.controller import user_controller as ctrl
@auth.route('/nurse/add',methods=['POST'])
def sign_up():
    try:
        resp = ctrl.save_user(request)
        return jsonify(resp)
    except Exception, e:
        print(e)
        return jsonify(status='error',
                       message="Error in saving  users")
@auth.route('/nurse/update',methods=['POST'])
def update_user():
    try:
        resp = ctrl.update_user(request)
        print(resp)
        return jsonify(resp)
    except Exception, e:
        print(e)
        return jsonify(status='error',
                       message="Error in updating  users")
@auth.route('/getNurse', methods = ['POST'])
def getNurse():
    try:
        resp = ctrl.get_user(request)
        return jsonify(resp)
    except Exception,e:
        print(e)
        return jsonify(status='error',
                       message="Error in getting Nurse")
@auth.route('/login', methods =['POST'])
def login():
    try:
        return jsonify(status= 'success')
    except Exception, e:
        return jsonify(status = 'error', message="Error in login" )