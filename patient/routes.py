from flask import Blueprint, request, jsonify
patient = Blueprint('patienturls', __name__)
from patient.controller import patient_controller as ctrl
from shared.util import *

@patient.route('/addPatient', methods= ['POST'])
@is_admin_doctor_nurse
def add_patient():
    try:
        resp = ctrl.save_patient(request)
        return jsonify(resp)
    except Exception,e :
        print(e)
        return jsonify(status='error',
                       message="Error in saving  patients")
@patient.route('/getPatients', methods = ['POST'])
@is_admin_doctor_nurse
def get_patients():
    try:
        resp = ctrl.get_patients(request)
        return jsonify(resp)
    except Exception,e :
        print(e)
        return jsonify(status='error',
                       message="Error in getting Nurse")
@patient.route('/updatePatient', methods = ['POST'])
@is_admin_doctor_nurse
def update_patients():
    try:
        resp = ctrl.update_patient(request)
        return jsonify(resp)
    except Exception,e :
        print(e)
        return jsonify(status='error',
                       message="Error in updating  patient")

