from typing import Annotated, Union

from pydantic import AwareDatetime, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

PhoneNumberType = Annotated[
    Union[str, PhoneNumber],
    PhoneNumberValidator(default_region='GB')
]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Reporter(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    job_title: str
    phone_number: PhoneNumber
    organization_name: str
    organization_address: str
    registration_date: AwareDatetime
