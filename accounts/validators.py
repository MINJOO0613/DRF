from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework.serializers import ValidationError
from .models import User

# 회원가입 시, validator
def validate_signup(user_data):
    err_msg = []

    # validation_username
    if username := user_data.get("username"):
        if User.objects.filter(username=username).exists():
            err_msg.append({"username":'이미 존재하는 아이디입니다.'})

    # validation_password    
    password = user_data.get("password")
    password2 = user_data.get("password2")
    if not password == password2:
        err_msg.append({'password':'비밀번호가 일치하지 않습니다.'})

    # validation_email
    if email := user_data.get("email"):
        if User.objects.filter(email=email).exists():
            err_msg.append({"email":'이미 존재하는 이메일입니다.'})
        else:
            try:
                validate_email(email)
            except:
                err_msg.append({'email':'이메일 형식이 올바르지 않습니다.'})
    
    # 에러메시지
    if err_msg:
        return False, err_msg 

    return True, err_msg


# 비밀번호 변경 시, validator
def validate_password_change(user, password_data):
    old_password = password_data.get("old_password")
    new_password = password_data.get("new_password")
    new_password2 = password_data.get("new_password2")

    err_msg = []

    # validation_password DB에 있는지 확인
    if not check_password(old_password, user.password):
            err_msg.append({"old_password":"비밀번호가 틀렸습니다."})
        
    # validation_새 비밀번호가 이전 비밀번호와 일치하지 않아야 함
    if old_password == new_password:
            err_msg.append({"new_password":"새로운 비밀번호를 입력해주세요."})

    # validation_new_password 1,2 일치한지 확인
    if new_password != new_password2 :
        err_msg.append({"new_password":"비밀번호가 일치하지 않습니다."})

    # settings에 있는 validator 사용한 유효성 검사 (비밀번호 자체에 대한 유효성 검사사)
    try:
        validate_password(new_password, user)
    except ValidationError as e:
        err_msg.append({"new_password": str(e)})

    if err_msg:
        return False, err_msg 

    return True, err_msg


# 프로필 수정 시, validator (회원정보 수정)
def validate_profile(user_data):
    err_msg = []

    # validation_username
    if username := user_data.get("username"):
        if User.objects.filter(username=username).exists():
            err_msg.append({"username":'이미 존재하는 아이디입니다.'})

    # validation_email
    if email := user_data.get("email"):
        if User.objects.filter(email=email).exists():
            err_msg.append({"email":'이미 존재하는 이메일입니다.'})
        else:
            try:
                validate_email(email)
            except:
                err_msg.append({'email':'이메일 형식이 올바르지 않습니다.'})

    # 에러메시지
    if err_msg:
        return False, err_msg 

    return True, err_msg