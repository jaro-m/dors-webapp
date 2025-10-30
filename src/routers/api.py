from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, desc, select

from ..db import get_session
from ..dependencies import get_current_user
from ..helpers import logger
from ..models import (
    Disease,
    DiseaseBase,
    Patient,
    PatientBase,
    Report,
    ReportBase,
    ReportResponse,
    Reporter,
    ReporterBase,
    ReportStatus,
)

router = APIRouter(prefix="/api")

SessionDep = Annotated[Session, Depends(get_session)]


@router.post(
    "/reports", summary="Create new report", tags=["reports"]
)
async def create_report(
    report: ReportBase,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
):
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
    id: int,
    reporter: ReporterBase,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
) -> Reporter:
    logger.info(f"reporter ID: {id}, reporter data: {reporter}")
    reporter_db = session.get(Reporter, id)

    try:
        if not reporter_db:
            # Creating a new Reporter
            reporter_db = Reporter(
                **reporter.model_dump(),
                id=id,
                date_registration=datetime.now()
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
async def create_patient(
    id: int,
    patient: PatientBase,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
) -> Patient:
    logger.info(f"POST /reports/{id}/patient")
    patient_db = session.get(Patient, id)

    try:
        if not patient_db:
            # Creating a new Patient
            patient_db = Patient(
                **patient.model_dump(),
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

    return patient_db


@router.post(
    "/reports/{id}/disease", summary="Add / update disease details", tags=["disease"]
)
async def create_disease(
    id: int,
    disease: DiseaseBase,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
) -> Disease:
    logger.info(f"Create Disease endpoint, ID: {id}")
    disease_db = session.get(Disease, id)

    try:
        if not disease_db:
            print("--------creating a new one----------")
            # Creating a new Disease record
            disease_db = Disease(
                **disease.model_dump(),
                id=id,
                date_created=datetime.now(),
                created_by=1
            )
            session.add(disease_db)
            session.commit()
            session.refresh(disease_db)

            logger.info(
                f"Disease <{disease.name}> successfully created"
            )
        else:
            print("-------- updating an existing one ----------")
            # Updating an existing Disease
            disease_data = disease.model_dump(exclude_unset=True)
            # leave this date unchanged
            disease_data["date_detected"] = disease_db.date_detected
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
async def update_report(
    id: int,
    report: ReportBase,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
):
    logger.info(f"Updating Report with ID: {id}")
    report_db = session.get(Report, id)

    if not report_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Report does not exist"),
        )

    if report_db.status != ReportStatus.draft:
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

    if report_db.status != ReportStatus.draft:
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


@router.get("/reports/recent", summary="Recent submissions", tags=["reports"])
async def get_recent(
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
) -> ReportResponse:
    logger.info("Recent submission")
    # try:
    # Is it only going to return "Submitted" reports?
    report = session.exec(
        select(Report)
            .where(Report.status == ReportStatus.submitted)
            .order_by(desc(Report.date_updated))
    ).first()
    reporter = (
        session.exec(select(Reporter).where(Reporter.id == report.reporter_id)).first()
    )
    patient = session.exec(select(Patient).where(Patient.id == report.patient_id)).first()
    disease = session.exec(select(Disease).where(Disease.id == report.disease_id)).first()
    print(f"{reporter}\n{patient}\n{disease}")
    print()
    # except Exception as err:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(err),
    #     ) from None
    raport_data = ReportResponse(
        **{
            **report.model_dump(),
            "reporter": reporter,
            "patient": patient,
            "disease": disease
        }
    )
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str("Reports do not exist"),
        )

    return raport_data


@router.get("/reports/{id}", summary="Get specific report", tags=["reports"])
async def get_report(
    id: int,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
) -> ReportResponse:
    try:
        report = session.get(Report, id)
        reporter = (
            session.exec(
                select(Reporter).where(Reporter.id == report.reporter_id)
            ).first()
        )
        patient = (
            session.exec(select(Patient).where(Patient.id == report.patient_id)).first()
        )
        disease = (
            session.exec(select(Disease).where(Disease.id == report.disease_id)).first()
        )
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

    report_data = ReportResponse(
        **{
            **report.model_dump(),
            "reporter": reporter,
            "patient": patient,
            "disease": disease
        }
    )

    return report_data


@router.get("/reports", summary="List reports (paginated)", tags=["reports"])
async def get_reports(
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
    offset: int = 0,
    limit: Annotated[int, Query(le=20)] = 20,
) -> list[ReportResponse]:
    try:
        reports = session.exec(select(Report).offset(offset).limit(limit)).all()
        all_results = []
        reporter_ids = set()
        patient_ids = set()
        disease_ids = set()

        for report in reports:
            reporter_ids.add(report.reporter_id)
            patient_ids.add(report.patient_id)
            disease_ids.add(report.disease_id)

        reporters = (
            session.exec(select(Reporter).where(Reporter.id.in_(reporter_ids)))
            .all()
        )
        patients = (
            session.exec(select(Patient).where(Patient.id.in_(patient_ids)))
            .all()
        )
        diseases = (
            session.exec(select(Disease).where(Disease.id.in_(disease_ids)))
            .all()
        )

        for report in reports:
            reporter = [r for r in reporters if r.id == report.reporter_id][0]
            patient = [p for p in patients if p.id == report.patient_id][0]
            disease = [d for d in diseases if d.id == report.disease_id][0]
            all_results.append(ReportResponse(
                **{
                    **report.model_dump(),
                    "reporter": reporter,
                    "patient": patient,
                    "disease": disease,
                }
            ))

    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="DB data inconsistency"
        ) from None
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

    return all_results


@router.get("/reports/{id}/reporter", summary="Get reporter details", tags=["reporter"])
async def get_reporter(
    id: int,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
) -> Reporter:
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
async def get_patient(
    id: int,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
):
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
async def get_disease(
    id: int,
    session: SessionDep,
    current_user: Annotated[ReporterBase, Depends(get_current_user)],
):
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
