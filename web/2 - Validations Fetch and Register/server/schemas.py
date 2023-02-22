"""
In this module we define the Pydantic models. While these models are
used to interface FastAPI with http clients, SQLAlchemy models 
are used to talk to the database.
NOTE: There will some code duplication because some attributes will
have to be defined twice, once for the Pydantic models, and once for
SQLAlchemy. In another coming example, we will introduce a new library
that will bridge the two libraries, and prevent some of the code
duplication that happens when you use Pydantic and SQLAlchemy
separately.
We will create an PlayerBase Pydantic models (or let's say "schemas") 
to have common attributes while creating or reading data.
And create an PlayerRegister that inherit from it (so they will have 
the same attributes), plus any additional data (attributes) needed for
creation.
So, the user will also have a password when creating it. But for 
security, the password won't be in other Pydantic models, for example,
it won't be sent from the API when reading a user.
"""

from enum import Enum

from pydantic import BaseModel, Field


class PlayerRegister(BaseModel):
    full_name: str
    email: str
    password: str
    phone_number: str | None = Field(
        title="Local portuguese phone number or international prefixed w/ +XYZ country code"
    )
    birth_date: str | None
    level: str
    tournament_id: int | None
#: