from flask import Blueprint, request, jsonify
auth = Blueprint('urls', __name__)
from auth.controller import user_controller as ctrl
from shared.util import *
@auth.route('/signUp',methods=['POST'])
def sign_up():
    try:
        resp = ctrl.save_user(request, role = 'admin')
        return jsonify(resp)
    except Exception, e:
        print(e)
        return jsonify(status='error',
                       message="Error in saving  users")
@auth.route('/nurse/add',methods=['POST'])
@is_admin
def add_nurse():
    try:
        resp = ctrl.save_user(request, role ='nurse')
        return jsonify(resp)
    except Exception, e:
        print(e)
        return jsonify(status='error',
                       message="Error in saving  users")

@auth.route('/nurse/update',methods=['POST'])
@is_admin
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
@is_admin
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
        resp = ctrl.validate_user(request)
        print(resp)
        return jsonify(resp)
    except Exception, e:
        print(e)
        return jsonify(status = 'error', message="Error in login" )