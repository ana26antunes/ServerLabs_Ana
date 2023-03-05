from fastapi import APIRouter
from fastapi_chameleon import template

router = APIRouter()

@router.get("/")
@template(template_file='index.html')
async def index(course1: str):
    return{
        'course1': 'course1',
        'course2': 'Contabilidade',
        'course3': 'Electronica',
    }
#:

@app.get("/about")
async def about():
    return{}
#: