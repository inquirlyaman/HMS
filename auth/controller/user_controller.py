from auth.models import *
from db.database import Base,Engine,session_context
from shared.util import *

def save_user(request):
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    if  not name :
        return dict(status='error', message="Name can not be empty")
    if not email :
        return dict(status='error', message="Email ids can't be empty")
    if email :
        status = validate_email(email.strip())
        if(status['status'] == 'error'):
            return status
    if password and confirm_password:
        status = valid_password(password.strip(),confirm_password.strip())   
        if(status['status'] == 'error'):
            return status 
    with session_context() as dbsession:
        hash_password = password_hash(password)
        hash_confirm_password = password_hash(confirm_password)
        user = User(name,email,hash_password,hash_confirm_password)
        dbsession.add(user)
        dbsession.commit()
        role = Roles("nurse")
        dbsession.add(role)
        dbsession.commit()
        user_roles = UserRoles(role.id,user.id)
        dbsession.add(user_roles)
        return dict(status='success', role = role.name)


    

