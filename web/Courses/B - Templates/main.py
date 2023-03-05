from fastapi import FastAPI
from fastapi_chameleon import global_init
import uvicorn

from views import (
    home,
    courses,
    account,
)

app = FastAPI()

def main():
    config()
    start_server()
    
    
def config():
    print("Configuring server")
    config_routes()
    config_templates()
    print("Done Configuring server")
    
def config_routes():
    for view in [home, courses, account]:
        app.include_router(view.router)
    
def config_templates():    
    global_init('templates')
    
def start_server():
    print("Now Starting server")
    uvicorn.run(app)
   


if __name__== '__main__':
    main()
    
else:
    config()
    
    
    