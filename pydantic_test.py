from pydantic import BaseModel, Field, EmailStr , field_validator


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

    age: int = Field(
        gt=18, lt=60, description="Age must be greater than 18 and less than 60"
    )

    email: EmailStr

    is_active: bool = True

    bio: str | None = Field(
        default=None, max_length=100, description="Optional short bio"
    )
    
    @field_validator('username')
    @classmethod
    def capitalize(cls , value):
        return value.upper()


def Signup(payload: User):
    print(payload.username)
    print(payload.password)
    print(payload.age)
    print(payload.email)
    print(payload.is_active)
    print(payload.bio)


data = {
    "username": "zulkaif_123",
    "password": "mypassword",
    "age": 22,
    "email": "zulkaif@gmail.com",
    "bio": "I am MERN Stack Developer",
}

user = User(**data)

Signup(user)
