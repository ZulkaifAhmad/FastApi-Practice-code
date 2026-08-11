from pydantic import BaseModel, Field, EmailStr , field_validator , model_validator , computed_field
from typing import Dict

class User(BaseModel):
    username: str = Field(
        min_length=4,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Only letters, numbers, and underscore allowed",
    )

    password: str = Field(
        min_length=6,
        max_length=30,
        description="Password must be between 6 and 30 characters",
    )

    age: int 

    email: EmailStr

    is_active: bool = True

    bio: str | None = Field(
        default=None, max_length=100, description="Optional short bio"
    )
    contact : Dict[str , str]
    # Height is provided in centimetres and weight in kilograms.
    height_cm: float = Field(gt=0)
    weight_kg: float = Field(gt=0)
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls , model):
        if model.age >= 60 and 'emergency_contact' not in model.contact:
            raise ValueError('user older then 60age must have emergency number')
        return model
    
    @field_validator('username')
    @classmethod
    def capitalize(cls , value):
        return value.upper()
    
    @computed_field
    @property
    def bmi(self) -> float:
        height_in_meters = self.height_cm / 100
        return round(self.weight_kg / (height_in_meters ** 2), 2)



def Signup(payload: User):
    print(payload.username)
    print(payload.password)
    print(payload.age)
    print(payload.email)
    print(payload.is_active)
    print(payload.bio)
    print('bmi',payload.bmi)


data = {
    "username": "zulkaif_123",
    "password": "mypassword",
    "age": 62,
    "email": "zulkaif@gmail.com",
    'contact' : {'phone':'0340' , 'emergency_contact' : '04534'} ,
    "bio": "I am MERN Stack Developer",
    'height_cm': 182.88,  # 6 feet
    'weight_kg': 72
}

user = User(**data)

Signup(user)
