from fastapi import APIRouter, Request
from fastapi_chameleon import template
from fastapi import responses
from fastapi import status

from services import student_service

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

from infrastructure.viewmodel import base_viewmodel_with



router = APIRouter()


@router.get('/account/register')                            # type: ignore
@template()
async def register():
    return register_viewmodel()
#:

def register_viewmodel():
    return base_viewmodel_with({
        'name':'',
        'email': '',
        'password': '',
        'birth_date': '',
        'min_date': MIN_DATE,
        'max_date': date.today(),
        'checked': False,
    })
#:

@router.post('/account/register')                            # type: ignore
@template(template_file='account/register.pt')
async def post_register(request: Request):
    vm = await post_register_viewmodel(request)
    if vm['error']:
        return vm
    response = responses.RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
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

    
        
        return base_viewmodel_with({
            'error': error,
            'error_msg': error_msg,
            'name': name,
            'email': email,
            'password': password,
            'birth_date':birth_date,
            'min_date': MIN_DATE,
            'max_date': date.today,
            'checked': False,
            'user_id': new_student_id,
            
        })
#:

@router.get('/account/login')                            # type: ignore
@template()
async def login():
    return login_viewodel()
#:

def login_viewodel():
    return base_viewmodel_with({
        'error': False,
        'error_msg': 'There was an error with your data. Please try again.'
    })
#:

@router.get('/account')               # type: ignore
@template()          
async def index():
    return account_viewmodel()
#:

def account_viewmodel():
    student = Student(
        id = 15_001,
        name = 'Alberto Antunes',
        email ='alb@mail.com',
        password = 'abc', 
        birth_date = date(1995,2,3),
    )
    
    
    return base_viewmodel_with({
        'name':student.name,
        'email':student.email,
    })
#: