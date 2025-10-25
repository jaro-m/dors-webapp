from datetime import datetime, timedelta
from enum import Enum as PyEnum
from typing import Annotated, Union

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator
# from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel import Enum, Field, SQLModel

PhoneNumberType = Annotated[
    Union[str, PhoneNumber],
    PhoneNumberValidator(default_region='GB')
]


class Gender(PyEnum):
    female = "Female"
    male = "Male"
    other = "Other"


class DiseaseCategory(PyEnum):
    bacterial = "Bacterial"
    viral = "Viral"
    parasitic = "Parasitic"
    other = "Other"


class SeverityLevel(PyEnum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


class TreatmentStatus(PyEnum):
    none = "None"
    ongoing = "Ongoing"
    completed = "Completed"


class RaportState(PyEnum):
    draft = "Draft"
    submitted = "Submitted"
    under_review = "Under Review"
    approved = "Approved"


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str | None = Field(default=None)
    username: str
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Reporter(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str = Field(nullable=False, max_length=50)
    last_name: str = Field(nullable=False, max_length=50)
    email: EmailStr = Field(unique=True, nullable=False)
    job_title: str = Field(nullable=False, max_length=100)
    phone_number: PhoneNumber = Field(nullable=False)
    organization_name: str = Field(nullable=False, max_length=200)
    organization_address: str = Field(nullable=False, max_length=500)
    # autopopulated (required)
    registration_date: datetime = Field(nullable=True)


class Patient(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str = Field(nullable=False, max_length=50)
    last_name: str = Field(nullable=False, max_length=50)
    date_of_birth: datetime = Field(nullable=False)
    # autopopulated (required)
    age: timedelta = Field(nullable=True)
    gender: PyEnum = Field(Enum(Gender), nullable=False)
    medical_record_number: int = Field(unique=True)
    patient_address: str = Field(nullable=False, max_length=500)
    emergency_contact: str = Field(nullable=True, max_length=200)


class Disease(SQLModel, table=True):
    id: int = Field(primary_key=True)
    disease_name: str = Field(nullable=False, max_length=100)
    disease_category: PyEnum = Field(Enum(DiseaseCategory), nullable=False)
    date_detected: datetime = Field(nullable=False)
    symptoms: str = Field(nullable=False)
    severity_level: PyEnum = Field(Enum(SeverityLevel), nullable=False)
    lab_results: str = Field(nullable=True)
    treatment_status: PyEnum = Field(Enum(TreatmentStatus), nullable=False)


class Report(SQLModel, table=True):
    id: int = Field(primary_key=True)
    state: PyEnum = Field(Enum(RaportState), nullable=False)

    reporter_id: int | None = Field(default=None, foreign_key="reporter.id")
    patient_id: int | None = Field(default=None, foreign_key="patient.id")
    disease_id: int | None = Field(default=None, foreign_key="disease.id")
