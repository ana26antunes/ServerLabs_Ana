from decimal import Decimal as dec
from dataclasses import dataclass

@dataclass
class Course:
    id: int
    category: str
    price: dec
    name: str
    summary: str
    description: str
    trainer_id: int
    trainer_name: str
    schedule: str
    available_seats: int
#:


@dataclass
class Trainer:
    id: int
    name: str
    expertise: str
    presentation: str
    twitter: str
    facebook: str
    instagram: str
    linkedin: str
#: