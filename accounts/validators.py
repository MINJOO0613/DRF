from django.core.validators import validate_email
from .models import User

def validate_signup(signup_data):
    username = signup_data.get("username")
    password = signup_data.get("password")
    password2 = signup_data.get("password2")
    first_name = signup_data.get("first_name")
    last_name = signup_data.get("last_name")
    email = signup_data.get("email")
    nickname = signup_data.get("nickname")
    date_of_birth = signup_data.get("date_of_birth")

    err_msg = []

    # validation_username
    if User.objects.filter(username=username).exists():
        err_msg.append('이미 존재하는 아이디입니다.')

    # validation_password
    if not password == password2:
        err_msg.append('비밀번호가 일치하지 않습니다.')

    # validation_email
    try:
        validate_email(email)
    except:
        err_msg.append('이메일 형식이 올바르지 않습니다.')
    
    if err_msg:
        return False, err_msg 

    return True, err_msg