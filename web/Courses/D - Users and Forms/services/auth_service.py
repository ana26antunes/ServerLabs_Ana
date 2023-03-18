

from fastapi import Response


AUTH_COOKIE_NAME = 'user_id'
SESSION_COOKIE_MAX_AGE = 86400_00

def set_auth_cookie(response: Response, user_id: int):
    cookie_value = f'{user_id}'
    response.set_cookie(
        AUTH_COOKIE_NAME,
        cookie_value,
        secure = False,      # True => que a cookie só é enviada por HTTPs
        httponly = True,
        samesite = 'lax',
        max_age = SESSION_COOKIE_MAX_AGE,
    )
#: