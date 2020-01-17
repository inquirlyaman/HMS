from patient.models import *
from db.database import Base,Engine,session_context
from shared.util import *

######## save_patient ##########
def save_patient(request):
    name = request.json.get("name")
    email = request.json.get("email")
    mobile = request.json.get("mobile")
    address = request.json.get("address")
    sex = request.json.get("sex")
    age = request.json.get("age")
    blood_group = request.json.get("blood_group")
    if  not name :
        return dict(status='error', message="Name can't be empty")
    if not email :
        return dict(status='error', message="Email ids can't be empty")
    if email :
        status = validate_email(email.strip())
        if(status['status'] == 'error'):
            return status
    if not mobile:
        return dict(status='error', message="Mobile numbers can't be empty")
    if mobile :
        status = validate_mobile(mobile.strip())
        if(status['status'] == 'error'):
            return status
   
    with session_context() as dbsession:
        
        patient = Patient(name, email,mobile,address,sex,age,blood_group)
        dbsession.add(patient)
        dbsession.commit()
        
        return dict(status='success', message = "Patient added successfully")
######get patient#######
def get_patients(request):
    patient_info = []
    per_page = int(request.json.get('per_page', 9))
    page_num = int(request.json.get('page_num',1))
    with session_context() as dbsession:
        offset = ( per_page * page_num) - per_page
        patients = dbsession.query(Patient).offset(offset).\
                         limit(per_page).all()
        total = dbsession.query(Patient).count()
        for patient in patients:
            patient_info.append(patient_json(patient))
        return dict(status='success',
                    patients=patient_info,
                    total=total)
######return patient json######
def patient_json(patient):
        info = {}
        info['id'] = patient.id
        info['name'] = patient.name
        info['email'] = patient.email
        info['mobile'] = patient.mobile
        info['address'] = patient.address
        return info
######## update_user ##########
def update_patient(request):
    patient_id = request.json.get("id")
    name = request.json.get("name")
    email = request.json.get("email")
    mobile = request.json.get("mobile")
    address = request.json.get("address")
    sex = request.json.get("sex")
    age = request.json.get("age")
    blood_group = request.json.get("blood_group")
    if  not name :
            return dict(status='error', message="Name can not be empty")
    if not email :
        return dict(status='error', message="Email ids can't be empty")
    if email :
        status = validate_email(email.strip())
        if(status['status'] == 'error'):
            return status
    
    with session_context() as dbsession:
        patient = dbsession.query(Patient).filter_by(id = patient_id).first()
        
        #1. Check if patient is present
        if patient is None:
            return dict(status="error", 
                            message="Invalid patient Id")
        patient.name = name
        patient.email = email
        patient.mobile = mobile
        patient.address = address
        patient.sex = sex
        patient.age = age
        patient.blood_group = blood_group
        dbsession.commit()
        return dict(status='success', patient= patient_json(patient),  message=" Patient updated successfully" )