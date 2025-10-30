from datetime import datetime
from enum import Enum as PyEnum
from typing import Annotated, Union

from pydantic import EmailStr, computed_field, validator
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator
from sqlalchemy import INTEGER, cast
from sqlalchemy.orm import column_property, declared_attr
from sqlmodel import (
    Column,
    Enum,
    FetchedValue,
    Field,
    ForeignKey,
    Relationship,
    SQLModel,
    TIMESTAMP,
    text,
)

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


class ReportStatus(PyEnum):
    draft = "Draft"
    submitted = "Submitted"
    under_review = "Under Review"
    approved = "Approved"


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class UserBase(SQLModel):
    username: str
    # additional attributes
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None


class User(UserBase, table=True):
    __table_args__ = {'extend_existing': True}

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str | None = Field(default=None)


class ReporterBase(SQLModel):
    username: str = Field(nullable=False)
    hashed_password: str | None
    first_name: str = Field(nullable=False, max_length=50)
    last_name: str = Field(nullable=False, max_length=50)
    email: EmailStr = Field(unique=True, nullable=False)
    job_title: str = Field(nullable=False, max_length=100)
    phone_number: PhoneNumber = Field(nullable=False)
    organization_name: str = Field(nullable=False, max_length=200)
    organization_address: str = Field(nullable=False, max_length=500)


class Reporter(ReporterBase, table=True):
    __table_args__ = {'extend_existing': True}

    id: int = Field(primary_key=True)
    date_registration: datetime = Field(nullable=False)

    reports: list["Report"] = Relationship(
        back_populates="reporter",
        sa_relationship=ForeignKey("report.id"),
        cascade_delete=True,
    )


class PatientBase(SQLModel):
    first_name: str = Field(nullable=False, max_length=50)
    last_name: str = Field(nullable=False, max_length=50)
    date_of_birth: datetime = Field(nullable=False)
    gender: Gender = Field(Enum(Gender))
    medical_record_number: int = Field(unique=True)
    patient_address: str = Field(nullable=False, max_length=500)
    emergency_contact: str = Field(nullable=True, max_length=200)


class Patient(PatientBase, table=True):
    __table_args__ = {'extend_existing': True}

    id: int | None = Field(primary_key=True)

    @validator('date_of_birth')
    def check_date(cls, value):
        if value > datetime.now():
            raise ValueError("DoB date cannot be in the future.")
        return value

    @computed_field(return_type=int)
    @declared_attr
    def age(self):
        return column_property(
            cast((datetime.now() - self.date_of_birth), INTEGER)
            )


class DiseaseBase(SQLModel):
    name: str = Field(nullable=False, max_length=100)
    category: DiseaseCategory = Field(Enum(DiseaseCategory), nullable=False)
    date_detected: datetime = Field(nullable=False)
    symptoms: str = Field(nullable=False)
    severity_level: SeverityLevel = Field(Enum(SeverityLevel), nullable=False)
    lab_results: str = Field(nullable=True)
    treatment_status: TreatmentStatus = Field(Enum(TreatmentStatus), nullable=False)


class Disease(DiseaseBase, table=True):
    __table_args__ = {'extend_existing': True}

    id: int = Field(primary_key=True)

    created_by: int = Field(nullable=False, foreign_key="reporter.id")
    updated_by: int | None = Field(default=None, foreign_key="reporter.id")
    date_created: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ))
    date_updated: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=FetchedValue(),
        ))


class ReportBase(SQLModel):
    status: ReportStatus = Field(Enum(ReportStatus, nullable=False))

    patient_id: int | None = Field(default=None, nullable=True)
    disease_id: int | None = Field(default=None, nullable=True)


class Report(ReportBase, table=True):
    __table_args__ = {'extend_existing': True}

    id: int | None = Field(default=None, primary_key=True)

    date_created: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ))
    date_updated: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=FetchedValue(),
        ))
    patient_id: int | None = Field(default=None, foreign_key="patient.id")
    disease_id: int | None = Field(default=None, foreign_key="disease.id")
    updated_by: int | None = Field(default=None, foreign_key="reporter.id")
    reporter_id: int | None = Field(default=None, foreign_key="reporter.id")

    reporter: Reporter | None = Relationship(
        back_populates="report",
        sa_relationship=ForeignKey("reporter.id"),
    )


class ReportResponse(ReportBase):
    id: int
    date_created: datetime
    date_updated: datetime
    reporter_id: int
    patient_id: int
    disease_id: int
    reporter: Reporter
    patient: Patient
    disease: Disease
