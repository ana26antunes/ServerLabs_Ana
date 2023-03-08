from fastapi import APIRouter, Request
from starlette.requests import Request
from fastapi_chameleon import template

from services import course_service, student_service, trainer_service
from common import base_viewmodel_with



router = APIRouter()

POPULAR_COURSES_COUNT = 3
SELECTED_COURSES_COUNT = 3

@router.get('/')                            # type: ignore
@template()
async def index(response: Request):
    return index_viewmodel()





def index_viewmodel():
    return base_viewmodel_with( {
        'num_courses': course_service.course_count(),
        'num_students': student_service.student_count(),
        'num_trainers': trainer_service.trainer_count(),
        'num_events': 159,
        'popular_courses': course_service.most_popular_courses(POPULAR_COURSES_COUNT),
        'selected_trainers': trainer_service.selected_trainers(SELECTED_TRAINERS_COUNT) 
    })
#:

@router.get('/about')                        # type: ignore
@template()
async def about(request: Request):
    return about_viewmodel()


def about_viewmodel():
    return base_viewmodel_with({
        'num_courses': 99,
        'num_students': 2315,
        'num_trainers': 23,
        'num_events': 159,
        'testimonials': [
            {
                'user_id': 239,
                'user_name': 'Saul Goodman',
                'user_occupation': 'CEO & Founder',
                'text': 'Quidem odit voluptate, obcaecati, explicabo nobis corporis perspiciatis nihil doloremque eius omnis officia voluptates, facere saepe quas consequatur aliquam unde. Ab numquam reiciendis sequi.',
            },
            {
                'user_id': 1001,
                'user_name': 'Sara Wilson',
                'user_occupation': 'Designer',
                'text': 'Export tempor illum tamen malis malis eram quae irure esse labore quem cillum quid cillum eram malis quorum velit fore eram velit sunt aliqua noster fugiat irure amet legam anim culpa.',
            },
            {
                'user_id': 704,
                'user_name': 'Jena Karlis',
                'user_occupation': 'Store Owner',
                'text': 'Enim nisi quem export duis labore cillum quae magna enim sint quorum nulla quem veniam duis minim tempor labore quem eram duis noster aute amet eram fore quis sint minim.',
            },
            {
                'user_id': 1002,
                'user_name': 'Matt Brandon',
                'user_occupation': 'Freelancer',
                'text': 'Fugiat enim eram quae cillum dolore dolor amet nulla culpa multos export minim fugiat minim velit minim dolor enim duis veniam ipsum anim magna sunt elit fore quem dolore labore illum veniam.',
            },
            {
                'user_id': 1589,
                'user_name': 'John Larson',
                'user_occupation': 'Entrepreneur',
                'text': 'Quis quorum aliqua sint quem legam fore sunt eram irure aliqua veniam tempor noster veniam enim culpa labore duis sunt culpa nulla illum cillum fugiat legam esse veniam culpa fore nisi cillum quid.',
            },
        ]
    })
#:
