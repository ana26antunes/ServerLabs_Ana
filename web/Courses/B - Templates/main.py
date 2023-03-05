from fastapi import FastAPI
from fastapi_chameleon import global_init
import uvicorn

from views import (
    home,
    courses,
    account,
)

app = FastAPI()

for view in [home, courses, account]:
    app.include_router(view.router)
    
    
global_init('templates')


if __name__== '__main__':
    uvicorn.run(app)