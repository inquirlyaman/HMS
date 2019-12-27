from flask import Blueprint, request, jsonify
auth = Blueprint('urls', __name__)
from auth.controller import user_controller as ctrl
@auth.route('/sign_up',methods=['POST'])
def sign_up():
    try:
        resp = ctrl.save_user(request)
        return jsonify(resp)
    except Exception, e:
        return jsonify(status='error',
                       message="Error in saving  users")