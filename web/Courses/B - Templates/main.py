from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi_chameleon import template, global_init
import uvicorn

app = FastAPI()
global_init('templates')


@app.get("/")
@template(template_file='index.html')
async def index(course1: str):
    return{
        'course1': 'course1',
        'course2': 'Contabilidade',
        'course3': 'Electronica',
        
    }

#:


if __name__== '__main__':
    uvicorn.run(app)