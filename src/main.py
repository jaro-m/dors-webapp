import logging
from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from .db import engine, get_session
from .models import (
    Disease,
    DiseaseBase,
    Patient,
    PatientBase,
    Report,
    ReportBase,
    Reporter,
    ReporterBase,
    RaportStatus,
    Token,
    TokenData,
    User,
    UserInDB,
)

SECRET_KEY = getenv("SECRET_KEY", "somethingR43IIyS1lley")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# keep the tags in the defined order
tags_metadata = [
    {"name": "reporter"},
    {"name": "patient"},
    {"name": "disease"},
    {"name": "reports"},
]

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(redirect_slashes=True, openapi_tags=tags_metadata)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user(username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def get_user(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.username == username:
            return UserInDB(**user.dict())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception from None

    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", include_in_schema=False)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get("/items/", summary="Reads items for the current user")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post(
    "/reports", summary="Create new report", tags=["reports"]
)
async def create_report(report: ReportBase, session: SessionDep):
    logger.info("Creating new Report")

    try:
        # Creating a new Reporter
        report_db = Report(
            **report.dict(),
            date_created=datetime.now(),
            # TODO: Authorized user ID
            reporter_id=1,
        )
        session.add(report_db)
        session.commit()
        session.refresh(report_db)

        logger.info(
            "Report successfully created"
        )
    except IntegrityError as err:
        session.rollback()
        logger.error(str(err.args))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err.args[0]),
        ) from None
    except Exception as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    return report_db


@app.post(
    "/reports/{id}/reporter", summary="Add / update reporter details", tags=["reporter"]
)
async def create_reporter(
    id: int, reporter: ReporterBase, session: SessionDep
) -> Reporter:
    logger.info(f"reporter ID: {id}, reporter data: {reporter}")
    reporter_db = session.get(Reporter, id)

    try:
        if not reporter_db:
            # Creating a new Reporter
            reporter_db = Reporter(
                **reporter.dict(),
                id=id,
                registration_date=datetime.now()
            )
            session.add(reporter_db)
            session.commit()
            session.refresh(reporter_db)

            logger.info(
                f"Reporter {reporter.first_name} {reporter.last_name} successfully created"
            )
        else:
            # Updating an existing Reporter
            reporter_data = reporter.model_dump(exclude_unset=True)
            reporter_db.sqlmodel_update(reporter_data)
            session.add(reporter_db)
            session.commit()
            session.refresh(reporter_db)

            logger.info(
                f"Reporter {reporter.first_name} {reporter.last_name} successfully updated"
            )
    except IntegrityError as err:
        session.rollback()
        logger.error(str(err.args))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err.args[0]),
        ) from None
    except Exception as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    return reporter_db


@app.post(
    "/reports/{id}/patient", summary="Add / update patient details", tags=["patient"]
)
async def create_patient(id: int, patient: PatientBase, session: SessionDep):
    logger.info("POST /reports/{id}/patient endpoint with ID:", id)
    patient_db = session.get(Patient, id)

    try:
        if not patient_db:
            # Creating a new Patient
            patient_db = Patient(
                **patient.dict(),
                id=id,
            )
            session.add(patient_db)
            session.commit()
            session.refresh(patient_db)

            logger.info(
                f"Patient {patient.first_name} {patient.last_name} successfully created"
            )
        else:
            # Updating an existing Patient
            patient_data = patient.model_dump(exclude_unset=True)
            patient_db.sqlmodel_update(patient_data)
            session.add(patient_db)
            session.commit()
            session.refresh(patient_db)

            logger.info(
                f"Patient {patient.first_name} {patient.last_name} successfully updated"
            )
    except IntegrityError as err:
        session.rollback()
        logger.error(str(err.args))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err.args[0]),
        ) from None
    except Exception as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    return patient


@app.post(
    "/reports/{id}/disease", summary="Add / update disease details", tags=["disease"]
)
async def create_disease(id: int, disease: DiseaseBase, session: SessionDep) -> Disease:
    logger.info(f"Create Disease endpoint, ID: {id}")
    disease_db = session.get(Disease, id)

    try:
        if not disease_db:
            # Creating a new Disease record
            disease_db = Disease(
                **disease.dict(),
                id=id,
                date_created=datetime.now(),
                # TODO: add authentication to this endpoint and the user/creator data
                created_by=1
            )
            session.add(disease_db)
            session.commit()
            session.refresh(disease_db)

            logger.info(
                f"Disease <{disease.name}> successfully created"
            )
        else:
            # Updating an existing Disease
            disease_data = disease.model_dump(exclude_unset=True)
            # TODO: updated_by should come from authentication/authorization process
            disease_db.sqlmodel_update({
                **disease_data,
                "updated_by": 1,
                "date_updated": datetime.now()
            })
            session.add(disease_db)
            session.commit()
            session.refresh(disease_db)

            logger.info(
                f"Disease <{disease.name}> successfully updated"
            )
    except IntegrityError as err:
        session.rollback()
        logger.error(str(err.args))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err.args[0]),
        ) from None
    except Exception as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    return disease_db


@app.put("/reports/{id}", summary="Update report (draft only)", tags=["reports"])
async def update_report(id: int, report: ReportBase, session: SessionDep):
    logger.info(f"Updating Report with ID: {id}")
    report_db = session.get(Report, id)

    if not report_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Report does not exist"),
        )

    if report_db.status != RaportStatus.draft:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=str("Report cannot be modified"),
        )

    try:
        # Updating existing Report
        report_data = report.model_dump(exclude_unset=True)
        # TODO: updated_by should come from authentication/authorization process
        report_db.sqlmodel_update({
            **report_data,
            "updated_by": 1,
            "date_updated": datetime.now()
        })
        session.add(report_db)
        session.commit()
        session.refresh(report_db)

        logger.info(
            f"Report <{id}> successfully updated"
        )
    except IntegrityError as err:
        session.rollback()
        logger.error(str(err.args))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err.args[0]),
        ) from None
    except Exception as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    return report_db


@app.delete("/reports/{id}", summary="Delete report (draft only)", tags=["reports"])
async def delete_report(id: int, session: SessionDep):
    logger.info(f"Deleting Report with ID: {id}")
    report_db = session.get(Report, id)

    if not report_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Report does not exist"),
        )

    if report_db.status != RaportStatus.draft:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=str("Report cannot be modified"),
        )

    try:
        # Deleting existing Report
        session.delete(report_db)
        session.commit()

        statement = select(Report).where(Report.id == id)
        results = session.exec(statement)
        report_db = results.first()

        if report_db:
            raise Exception("Report was not deleted", report_db)

        logger.info(
            f"Report <{id}> successfully updated"
        )
    except Exception as err:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/reports/{id}", summary="Get specific report", tags=["reports"])
async def get_report(id: int, session: SessionDep):
    try:
        report = session.get(Report, id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Report does not exist"),
        )

    return report


@app.get("/reports", summary="List reports (paginated)", tags=["reports"])
async def get_reports(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=20)] = 20
) -> list[Report]:
    try:
        reports = session.exec(select(Report).offset(offset).limit(limit)).all()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    if not reports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Reports do not exist"),
        )

    return reports


@app.get("/reports/{id}/reporter", summary="Get reporter details", tags=["reporter"])
async def get_reporter(id: int, session: SessionDep) -> Reporter:
    try:
        reporter = session.get(Reporter, id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    if not reporter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Reporter does not exist"),
        )

    return reporter


@app.get("/reports/{id}/patient", summary="Get patient details", tags=["patient"])
async def get_patient(id: int, session: SessionDep):
    try:
        patient = session.get(Patient, id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Patient does not exist"),
        )

    return patient


@app.get("/reports/{id}/disease", summary="Get disease details", tags=["disease"])
async def get_disease(id: int, session: SessionDep):
    try:
        disease = session.get(Disease, id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        ) from None

    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("The Disease record was not found"),
        )

    return disease


#   ----- ENDPOINTS TO IMPLEMENT ------
# POST    /api/reports                # Create new report               +
# GET     /api/reports                # List reports (paginated)        +
# GET     /api/reports/{id}           # Get specific report             +
# PUT     /api/reports/{id}           # Update report (draft only)
# DELETE  /api/reports/{id}           # Delete report (draft only)

# POST    /api/reports/{id}/reporter  # Add/update reporter details     +
# GET     /api/reports/{id}/reporter  # Get reporter details            +
# POST    /api/reports/{id}/patient   # Add/update patient details      +
# GET     /api/reports/{id}/patient   # Get patient details             +
# POST    /api/reports/{id}/disease   # Add/update disease details      +
# GET     /api/reports/{id}/disease   # Get disease details             +

# POST    /api/reports/{id}/submit    # Submit report (change status)
# GET     /api/reports/search         # Search reports
# GET     /api/statistics             # Basic statistics

#   ----- ADVANCED -----
# GET     /api/reports/export/{format}  # Export data (CSV/JSON)
# GET     /api/diseases/categories    # Get disease categories
# GET     /api/reports/recent         # Recent submissions
