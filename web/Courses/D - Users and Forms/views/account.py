from fastapi import APIRouter, Request
from fastapi_chameleon import template
from fastapi import responses
from fastapi import status

from services import student_service
from services import auth_service
from data.models import Student
from datetime import date

from infrastructure.common import (
    is_valid_name,
    is_valid_email,
    is_valid_password,
    is_valid_birth_date,
    form_field_as_str,
    MIN_DATE,
)

from infrastructure.viewmodel import ViewModel



router = APIRouter()


@router.get('/account/register')                            # type: ignore
@template()
async def register():
    return register_viewmodel()
#:

def register_viewmodel() -> ViewModel:
    return ViewModel(
        name = '',
        email = '',
        password = '',
        birth_date ='',
        min_date = MIN_DATE,
        max_date = date.today,
        checked = False,
    )
#:

@router.post('/account/register')                            # type: ignore
@template(template_file='account/register.pt')
async def post_register(request: Request):
    vm = await post_register_viewmodel(request)
    
    if vm.error:
        return vm
    response = responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    auth_service.set_auth_cookie(response, vm.new_student_id)
    return response
#:

async def post_register_viewmodel(request: Request):
    form_data = await request.form()
    name = form_field_as_str(form_data, 'name')
    email = form_field_as_str(form_data,'email')
    password = form_field_as_str(form_data,'password')
    birth_date = form_field_as_str(form_data,'birth_date')
    new_student_id = None
    
    
    if not is_valid_name(name):
        error, error_msg = True, 'Invalid name!'
    #:
    elif not is_valid_email(email):    
        error, error_msg = True, 'Invalid email address!'
    elif not is_valid_password(password):    
        error, error_msg = True, 'Invalid password!'
    elif not is_valid_birth_date(birth_date):    
        error, error_msg = True, 'Invalid birthdate!'
    elif student_service.get_student_by_email(email):
        error, error_msg = True, f'Endereço de email {email} já foi resgistado!'
    else:
        error, error_msg = False, ''
        
    if not error:
        new_student_id = student_service.create_account(
            name,
            email,
            password,
            date.fromisoformat(birth_date),
         )

    
        
        return ViewModel(
            error = error,
            error_msg =  error_msg,
            name = name,
            email = email,
            password = password,
            birth_date =birth_date,
            min_date = MIN_DATE,
            max_date = date.today,
            checked = False,
            new_student_id = new_student_id,
            
        )
#:

@router.get('/account/login')                            # type: ignore
@template()
async def login():
    return login_viewodel()
#:

def login_viewodel():
    return ViewModel(
        email = '',
        password = ''
    )
#:

@router.post('/account/login')                            # type: ignore
@template(template_file='account/login.pt')
async def post_login(request: Request):
    vm = await post_login_viewmodel(request)

    if vm.error:
        return vm

    response = responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
    auth_service.set_auth_cookie(response, vm.student_id)
    return response
#:

async def post_login_viewmodel(request: Request) -> ViewModel:
    form_data = await request.form()
    form_data = await request.form()
    name = form_field_as_str(form_data, 'name')
    email = form_field_as_str(form_data,'email')
    password = form_field_as_str(form_data,'password')
    new_student_id = None,
    
    if not is_valid_email(email):
            error, error_msg = True, 'Invalid user or password!'
    #:
    elif not is_valid_password(password):    
        error, error_msg = True, 'Invalid password!'
        error, error_msg = True, 'Invalid password!'
    #:
    elif not (student := student_service.authenticate_student_by_email(email, password)):
       error, error_msg = True, 'User not found!'
    #:
    else:
      error, error_msg = False, ''
      student_id = student.id
    #:

    return ViewModel(
        error = error,
        error_msg =  error_msg,
        name = name,
        email = email,
        password = password,
        student_id = student_id,
    )
#:

@router.get('/account')               # type: ignore
@template()          
async def index():
    return account_viewmodel()
#:

@router.get('/account/logout')      # type: ignore
async def logout():        
    response = responses.RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)
    auth_service.delete_auth_cookie(response)
    return response
#:



def account_viewmodel() -> ViewModel:
    student = Student(
        id = 15_001,
        name = 'Alberto Antunes',
        email ='alb@mail.com',
        password = 'abc', 
        birth_date = date(1995,2,3),
    )
    
    
    return ViewModel(
        name = student.name,
        email = student.email,
    )
#: