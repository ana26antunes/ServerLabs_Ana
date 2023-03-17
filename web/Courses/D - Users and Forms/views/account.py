from fastapi import APIRouter
from fastapi_chameleon import template

from common import base_viewmodel_with

from data.models import Student
from datetime import date

router = APIRouter()



@router.get('/account/register')                            # type: ignore
@template()
async def register():
    return register_viewodel()
#:

def register_viewodel():
    return base_viewmodel_with({
        'error': False,
        'error_msg': 'There was an error with your data. Please try again.'
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
    return account_viewodel()
#:

def account_viewodel():
    student = Student(
        id = 15_001,
        name = 'Alberto Antunes',
        email ='alb@mail.com',
        password = 'abc', 
        birth_date = date(1995,2,3),
    )
    
    
    return base_viewmodel_with({
        'student_name':student.name,
        'student_email':student.email,
    })
#: