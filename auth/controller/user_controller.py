from auth.models import *
from db.database import Base,Engine,session_context
from shared.util import *
import jwt
import datetime
key = 'HMS'
######## save_user ##########
def save_user(request,role):
    name = request.json.get("name")
    email = request.json.get("email")
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    address = request.json.get("address")
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
        
    if password and confirm_password:
        status = valid_password(password.strip(),confirm_password.strip())   
        if(status['status'] == 'error'):
            return status 
    with session_context() as dbsession:
        hash_password = password_hash(password)
        hash_confirm_password = password_hash(confirm_password)
        user = User(hash_password,hash_confirm_password)
        dbsession.add(user)
        dbsession.commit()
        role = Roles(role)
        dbsession.add(role)
        dbsession.commit()
        user_roles = UserRoles(role.id,user.id)
        user_profiles = UserProfiles(name,email,mobile,address,user.id)
        dbsession.add(user_roles)
        dbsession.add(user_profiles)
        return dict(status='success', role = role.name)
    
######## update_user ##########
def update_user(request):
    name = request.json.get("name")
    email = request.json.get("email")
    mobile = request.json.get("mobile")
    address = request.json.get("address")
    user_id = request.json.get("id")
    if  not name :
            return dict(status='error', message="Name can not be empty")
    if not email :
        return dict(status='error', message="Email ids can't be empty")
    if email :
        status = validate_email(email.strip())
        if(status['status'] == 'error'):
            return status
    
    with session_context() as dbsession:
        user = dbsession.query(User).filter_by(id = user_id).first()
        user_profile =  dbsession.query(UserProfiles).filter_by(user_id = user.id).first()
        #1. Check if user is present
        if user is None:
            return dict(status="error", 
                            message="Invalid User Id")
        user.password = user.password
        user.confirm_password = user.confirm_password
        user_profile.name = name
        user_profile.mobile = mobile
        user_profile.email = email
        user_profile.address = address
        dbsession.commit()
        return dict(status='success', name = name,  message=" User updated successfully" )
######get user#######
def get_user(request):
    users_info = []
    per_page = int(request.json.get('per_page', 9))
    page_num = int(request.json.get('page_num',1))
    with session_context() as dbsession:
        offset = ( per_page * page_num) - per_page
        users = dbsession.query(UserProfiles).offset(offset).\
                         limit(per_page).all()
        total = dbsession.query(User).count()
        for user in users:
            users_info.append(user_json(user))
        return dict(status='success',
                    users=users_info,
                    total=total)
######validate  user#######
def validate_user(request):
    email = request.json.get('email')
    password = request.json.get('password')
    if not email :
        return dict(status='error', message="Email ids can't be empty")
    if not password:
        return dict(status ='error', message= "password can't be empty")
    if email :
        status = validate_email(email.strip())
        if(status['status'] == 'error'):
            return status
    with session_context() as dbsession:
        user_profile =  dbsession.query(UserProfiles).filter_by(email = email).first()
        user = dbsession.query(User).filter_by(id =user_profile.id).first()
        user_roles =  dbsession.query(UserRoles).filter_by(user_id = user.id).first()
        roles =  dbsession.query(Roles).filter_by(id = user_roles.role_id).first()
        if user is None or user_profile is None:
            return dict(status="error", 
                            message="Invalid User Id")
        if(verify_password(password, user.password)):
            access_token = jwt.encode({'user': action_token_object(user_profile,roles), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) }, key)
            return dict(access_token=access_token.decode('UTF-8')), 200
            
######return user json######
def user_json(user):
        info = {}
        info['id'] = user.user_id 
        info['name'] = user.name
        info['email'] = user.email
        info['mobile'] = user.mobile
        info['address'] = user.address
        return info
def action_token_object(user_profile,roles):
    info = {}
    info['name'] = user_profile.name
    info['role'] = roles.name
    return info
