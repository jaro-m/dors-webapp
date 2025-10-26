from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from ..db import get_session
from ..helpers import logger
from ..models import (
    Disease,
    DiseaseBase,
    Patient,
    PatientBase,
    Report,
    ReportBase,
    Reporter,
    ReporterBase,
    RaportStatus,
)

router = APIRouter(prefix="/api")

SessionDep = Annotated[Session, Depends(get_session)]


@router.post(
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


@router.post(
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
                f"Reporter {reporter.first_name} "
                f"{reporter.last_name} successfully created"
            )
        else:
            # Updating an existing Reporter
            reporter_data = reporter.model_dump(exclude_unset=True)
            reporter_db.sqlmodel_update(reporter_data)
            session.add(reporter_db)
            session.commit()
            session.refresh(reporter_db)

            logger.info(
                f"Reporter {reporter.first_name} "
                f"{reporter.last_name} successfully updated"
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


@router.post(
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


@router.post(
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


@router.put("/reports/{id}", summary="Update report (draft only)", tags=["reports"])
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


@router.delete("/reports/{id}", summary="Delete report (draft only)", tags=["reports"])
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


@router.get("/reports/{id}", summary="Get specific report", tags=["reports"])
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


@router.get("/reports", summary="List reports (paginated)", tags=["reports"])
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


@router.get("/reports/{id}/reporter", summary="Get reporter details", tags=["reporter"])
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


@router.get("/reports/{id}/patient", summary="Get patient details", tags=["patient"])
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


@router.get("/reports/{id}/disease", summary="Get disease details", tags=["disease"])
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
