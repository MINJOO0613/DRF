# **spartamarket_DRF**
Spartamarket_DRF는 **Django Rest Framework로 만드는 API** 입니다.

**사용자는 이 API를 통해 회원 가입, 로그인, 상품 등록 및 관리 기능**을 사용할 수 있습니다. 

**JWT 인증 방식**을 사용하며, **모든 사용자 정보와 상품 데이터는 안전하게 데이터베이스에 저장**됩니다.
<br/><br/><br/><br/>

## **개발 기간**
2024.09.01.~2024.09.10
<br/><br/><br/><br/>

## **개발 환경**
**Python :** Django DRF

**DB :** SQlite

- **JWT**: 사용자 인증 및 권한 관리
- **DRF:** Django 기반 REST API 구현
- **SQLite:** 간단한 로컬 데이터베이스
<br/><br/><br/><br/>


## **ERD**
![my_project_visualized](https://github.com/user-attachments/assets/7c066584-5b37-46d7-b4c5-1cf8e33b6db7)
<br/><br/><br/><br/>

## **Requirements**
```
Python==3.10.11
Django==4.2
```
- annotated-types==0.7.0
- anyio==4.4.0
- asgiref==3.8.1
- async-timeout==4.0.3
- attrs==24.2.0
- autopep8==2.3.1
- certifi==2024.8.30
- colorama==0.4.6
- distro==1.9.0
- **Django==4.2**
- django-extensions==3.2.3
- django-redis==5.4.0
- django-seed==0.3.1
- django-silk==5.2.0
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- drf-spectacular==0.27.2
- exceptiongroup==1.2.2
- Faker==28.0.0
- gprof2dot==2024.6.6
- h11==0.14.0
- httpcore==1.0.5
- httpx==0.27.2
- idna==3.8
- inflection==0.5.1
- jiter==0.5.0
- jsonschema==4.23.0
- jsonschema-specifications==2023.12.1
- openai==1.43.0
- pillow==10.4.0
- psycopg2==2.9.9
- pycodestyle==2.12.1
- pydantic==2.8.2
- pydantic_core==2.20.1
- pydotplus==2.0.2
- PyJWT==2.9.0
- pyparsing==3.1.4
- python-dateutil==2.9.0.post0
- PyYAML==6.0.2
- redis==5.0.8
- referencing==0.35.1
- rpds-py==0.20.0
- six==1.16.0
- sniffio==1.3.1
- sqlparse==0.5.1
- tomli==2.0.1
- toposort==1.10
- tqdm==4.66.5
- typing_extensions==4.12.2
- tzdata==2024.1
- uritemplate==4.1.1
<br/><br/><br/><br/>




## **설치 및 실행 방법**
**1. 클론 리포지토리**
```
git clone https://github.com/MINJOO0613/DRF
```


**2. 가상 환경 설정 및 활성화**
```
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```


**3.  필수 패키지 설치**
```
pip install -r requirements.txt
```


**4. 마이그레이션 적용 및 서버 실행**
```
python manage.py migrate
python manage.py runserver
```
<br/><br/><br/><br/>
## **RESTful API 명세서**
https://documenter.getpostman.com/view/38004701/2sAXjSyomz
**각 기능별 Postman에서 기능 점검하여 문서화함.**
<br/><br/><br/><br/><br/><br/>

## **기능 구현**
### **MVP(Minimum Viable Product)**

- **Refrresh Token**
    - **Endpoint**: **`/api/accounts/token/refresh`**
    - **Method**: **`POST`**
    - **검증**: 유효한 refresh_token으로 인증
    - **구현**: 사용자가 유효한 리프레시 토큰을 요청하여 새로운 access_token과 refresh_token을 발급.
- **회원가입**
    - **Endpoint**: **`/api/accounts`**
    - **Method**: **`POST`**
    - **조건**: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개는 생략 가능
    - **검증**: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
    - **구현**: 데이터 검증 후 저장.
- **회원 탈퇴**
    - **Endpoint**: **`/api/accounts`**
    - **Method**: **`DELETE`**
    - **조건**: 로그인 상태, 비밀번호 재입력 필요.
    - **검증**: 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
    - **구현**: 비밀번호 확인 후 계정 삭제.
- **로그인**
    - **Endpoint**: **`/api/accounts/login`**
    - **Method**: **`POST`**
    - **조건**: 사용자명과 비밀번호 입력 필요.
    - **검증**: 사용자명과 비밀번호가 데이터베이스의 기록과 일치해야 함.
    - **구현**: 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.
- **로그아웃**
    - **Endpoint**: **`/api/accounts/logout`**
    - **Method**: **`POST`**
    - **조건**: 로그인 상태 필요.
    - **구현**: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
- **패스워드 변경**
    - **Endpoint**: **`/api/accounts/password`**
    - **Method**: **`PUT`**
    - 조건: 기존 패스워드와 변경할 패스워드는 상이해야 함
    - 검증: 패스워드 규칙 검증
    - 구현: 패스워드 검증 후 데이터베이스에 업데이트.
- **프로필 조회**
    - **Endpoint**: **`/api/accounts/<str:username>`**
    - **Method**: **`GET`**
    - **조건**: 로그인 상태 필요.
    - **검증**: 로그인 한 사용자만 프로필 조회 가능
    - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.
- **회원정보 수정**
    - **Endpoint**: **`/api/accounts/<str:username>`**
    - **Method**: **`PUT`**
    - **조건**: 이메일, 이름, 닉네임, 생일 입력 필요하며, 성별, 자기소개는 생략 가능
    - **검증**: 로그인 한 사용자만 본인 프로필 수정 가능. 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안 됨.
    - **구현**: 입력된 정보를 검증 후 데이터베이스를 업데이트.

 <br/><br/><br/><br/>
### **상품 관련 기능**

- **상품 등록**
    - **Endpoint**: **`/api/products`**
    - **Method**: **`POST`**
    - **조건**: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
    - **구현**: 새 게시글 생성 및 데이터베이스 저장.
- **상품 목록 조회**
    - **Endpoint**: **`/api/products`**
    - **Method**: **`GET`**
    - **조건**: 로그인 상태 불필요.
    - **구현**: 모든 상품 목록 페이지네이션으로 반환.
- **상품 상세 조회**
    - **Endpoint**: **`/api/products/<int:productId>`**
    - **Method**: **`GET`**
    - **조건**: 로그인 상태 불필요.
    - **구현**: 상품 상세페이지 반환.
- **상품 수정**
    - **Endpoint**: **`/api/products/<int:productId>`**
    - **Method**: **`PUT`**
    - **조건**: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
    - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
    - **구현**: 입력된 정보로 기존 상품 정보를 업데이트.
- **상품 삭제**
    - **Endpoint**: **`/api/products/<int:productId>`**
    - **Method**: **`DELETE`**
    - **조건**: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
    - **검증**: 요청자가 게시글의 작성자와 일치하는지 확인.
    - **구현**: 해당 상품을 데이터베이스에서 삭제.
 
- **페이지네이션 및 필터링(검색기능)**
    - **조건**: 상품 목록 조회 시 적용됩니다.
 
<br/><br/><br/><br/>
### **데이터베이스 관계 모델링 기능**

- **팔로잉 시스템**
    - 사용자 간의 **ManyToMany** 관계를 통한 **팔로잉** 기능.
- **게시글 좋아요 기능**
    - 등록된 게시물 간의 **좋아요** 기능.
 
<br/><br/><br/><br/>
## **프로젝트 구조 섹션**
```
.
├─accounts
│  ├─migrations
│  │  └─__pycache__
│  ├─__pycache__
│  ├─__init__.py
│  ├─admin.py
│  ├─apps.py
│  ├─models.py
│  ├─serializerss.py
│  ├─tests.py
│  ├─urls.py
│  ├─validators.py
│  └─views.py
├─media
│  └─images
├─products
│  ├─migrations
│  │  └─__pycache__
│  ├─__pycache__
│  ├─__init__.py
│  ├─admin.py
│  ├─apps.py
│  ├─models.py
│  ├─pagination.py
│  ├─serializerss.py
│  ├─tests.py
│  ├─urls.py
│  └─views.py
├─spartamarket_DRF
│  ├─__pycache__
│  ├─__init__.py
│  ├─asgi.py
│  ├─settings.py
│  ├─urls.py
│  └─wsgi.py
├─manage.py
└──requirements.txt
```
<br/><br/><br/><br/>
## **트러블 슈팅(Troubleshootiong) 및 해결법**
**1. 설치 중 의존성 문제:**
- `pip install -r requirements.txt`를 실행할 때 특정 패키지 설치 오류가 발생할 수 있습니다. 이 경우, Python 버전 호환성 문제일 수 있으므로 README에 Python 버전을 명시하세요.

**2. 데이터베이스 마이그레이션 오류:**
- `python manage.py migrate` 실행 시 데이터베이스 마이그레이션 오류가 발생할 수 있습니다. 데이터베이스 파일이 누락되었거나 잘못된 경우일 수 있습니다. README에 `makemigrations` 및 `migrate` 명령어의 순서를 명시하고, SQLite 파일이 .gitignore에 추가되어 있는지 확인하세요.

**3. 토큰 인증 관련 문제:**
- JWT 인증 방식에서 토큰 만료 또는 블랙리스트 관리가 제대로 이루어지지 않을 경우 발생할 수 있습니다. 예를 들어, 토큰 만료 시 `401 Unauthorized` 응답이 반환되지 않는 문제 등. 이는 토큰 만료 시간 설정이나 토큰 블랙리스트 관리에서 발생할 수 있는 문제입니다.
- **해결책:** `settings.py`에서 `SIMPLE_JWT` 설정을 확인하고, 토큰의 만료 시간과 블랙리스트 기능이 활성화되어 있는지 점검합니다.

**4. 사용자 인증 관련 문제:**
- 로그인 또는 로그아웃 시 토큰이 올바르게 발급되지 않거나 무효화되지 않는 경우. 이는 토큰 발급 로직의 오류이거나, 잘못된 토큰을 사용한 경우 발생할 수 있습니다.
- **해결책:** `api/accounts/login` 및 `api/accounts/logout` 엔드포인트에서 사용되는 뷰를 점검하고, 토큰이 올바르게 관리되고 있는지 확인합니다.
