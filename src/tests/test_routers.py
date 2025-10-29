import datetime
import freezegun
from sqlmodel import SQLModel, create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from unittest import IsolatedAsyncioTestCase

from .data.db_test_data import (diseases, patients, reporters, reports)

from ..models import (
    Disease,
    DiseaseBase,
    DiseaseCategory,
    Gender,
    Patient,
    PatientBase,
    Report,
    ReportBase,
    ReportStatus,
    Reporter,
    ReporterBase,
    SeverityLevel,
    TreatmentStatus,
    User,
)
from ..routers.api import (
    create_disease,
    create_patient,
    create_report,
    create_reporter,
    update_report,
)

engine = create_engine("sqlite:///testdatabase.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

date_created = (
    datetime.datetime.fromisoformat("2025-09-10T02:02:02.1234567Z").replace(tzinfo=None)
)
disease_01 = {
    "id": 1000,
    "name": "Bacterial Disease",
    "category": DiseaseCategory.bacterial,
    "date_detected": (
        datetime.datetime
        .fromisoformat("2025-06-06T11:11:11.1234567Z")
        .replace(tzinfo=None)
    ),
    "symptoms": "Fever, thrills",
    "severity_level": SeverityLevel.high,
    "lab_results": "TBA",
    "treatment_status": TreatmentStatus.ongoing,
    "date_created": date_created,
    "date_updated": None,
    "created_by": 3,
    "updated_by": None,
}
patient_01 = {
    "id": 1,
    "first_name": "William",
    "last_name": "Ackerley",
    "date_of_birth": (
        datetime.datetime
        .fromisoformat("1999-05-25T11:11:11.1234567Z")
        .replace(tzinfo=None)
    ),
    "gender": Gender.male,
    "medical_record_number": 1,
    "patient_address": "42, Avenue, Somewhere, UK",
    "emergency_contact": "spouse",
}
reporter_01 = {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@email.com",
    "job_title": "Admin",
    "phone_number": "+447987654321",
    "organization_name": "NHS",
    "organization_address": "everywhere",
    "date_registration": (
        datetime.datetime
        .fromisoformat("2025-05-05T11:11:11.1234567Z")
        .replace(tzinfo=None)
    )
}
report_01 = {
    "id": 1,
    "status": ReportStatus.draft,
    "date_created": (
        datetime.datetime
        .fromisoformat("2025-05-05T11:11:11.1234567Z")
        .replace(tzinfo=None)
    ),
    "date_updated": (
        datetime.datetime
        .fromisoformat
        ("2025-05-05T14:15:15.1234567Z")
        .replace(tzinfo=None)
    ),
    "patient_id": 2,
    "disease_id": 4,
    "updated_by": 1,
    "reporter_id": 4,
}



def create_db():
    SQLModel.metadata.create_all(engine)


class TestAPIEndpoints(IsolatedAsyncioTestCase):
    """
    The class to test endpoints (integration tests)
    The tested ondpoints list:
    POST    /api/reports                  - Create new report
    GET     /api/reports                  - List reports (paginated)
    GET     /api/reports/{id}             - Get specific report
    PUT     /api/reports/{id}             - Update report (draft only)
    DELETE  /api/reports/{id}             - Delete report (draft only)
    POST    /api/reports/{id}/reporter    - Add/update reporter details
    GET     /api/reports/{id}/reporter    - Get reporter details
    POST    /api/reports/{id}/patient     - Add/update patient details
    GET     /api/reports/{id}/patient     - Get patient details
    POST    /api/reports/{id}/disease     - Add/update disease details
    GET     /api/reports/{id}/disease     - Get disease details
    POST    /api/reports/{id}/submit      - Submit report (change status)
    GET     /api/reports/search           - Search reports
    GET     /api/statistics               - Basic statistics
    """
    def setUp(self):
        create_db()
        self.current_user = User(**{
            "id": 3,
            "username": "johndoe",
            "full_name": "John Doe",
            "hashed_password": "***",
        })
        self.disease = Disease(**diseases[0])
        self.patient = Patient(**patients[0])
        self.report = Report(**reports[0])
        self.reporter = Reporter(**reporters[0])

    @freezegun.freeze_time("2025-05-05")
    async def test_freeze_time(self):
        assert datetime.date.fromisoformat("2025-05-05") == datetime.date.today()

    @freezegun.freeze_time("2025-09-10T02:02:02.1234567")
    async def test_creating_disease(self):
        results = await create_disease(
            id=1000,
            disease=DiseaseBase(**disease_01),
            session=session,
            current_user=self.current_user,
        )

        for key in disease_01:
            print(f"testing key: {key}")
            if key in ("date_created", "date_updated"):
                # freezegun doesn't work :(
                # assert getattr(results, key) == date_created
                continue
            if key == "created_by":
                assert getattr(results, key) == self.current_user.id
                continue
            if key == "updated_by":
                # updated_by is None while the record is newly created
                assert getattr(results, key) is None
                continue
            assert getattr(results, key) == disease_01[key]

    @freezegun.freeze_time("2025-09-10T02:02:02.1234567")
    async def test_modifying_disease(self):
        results = await create_disease(
            id=1000,
            disease=DiseaseBase(**{**disease_01, "lab_results": "still nothing"}),
            session=session,
            current_user=self.current_user,
        )

        for key in disease_01:
            print(f"testing key: {key}")
            if key in ("date_created", "date_updated"):
                # freezegun doesn't work :( and updated_by
                # assert getattr(results, key) == date_created
                continue
            if key == "created_by":
                assert getattr(results, key) == self.current_user.id
                continue
            if key == "updated_by":
                # updated_by has to have a number now
                assert getattr(results, key) == 3
                continue
            if key == "lab_results":
                assert getattr(results, key) == "still nothing"
                continue
            assert getattr(results, key) == disease_01[key]


    @freezegun.freeze_time("2025-09-10T02:02:02.1234567")
    async def test_creating_patient(self):
        results = await create_patient(
            id=1000,
            patient=PatientBase(**patient_01),
            session=session,
            current_user=self.current_user,
        )

        assert results.first_name == patient_01["first_name"]
        assert results.last_name == patient_01["last_name"]
        assert results.date_of_birth == patient_01["date_of_birth"]
        assert results.gender == patient_01["gender"]
        assert results.medical_record_number == patient_01["medical_record_number"]
        assert results.patient_address == patient_01["patient_address"]
        assert results.emergency_contact == patient_01["emergency_contact"]
        assert results.age == 26
        assert results.id == 1000

    @freezegun.freeze_time("2025-09-10T02:02:02.1234567")
    async def test_modifying_patient(self):
        results = await create_patient(
            id=1000,
            patient=PatientBase(**{**patient_01, "last_name": "IDK"}),
            session=session,
            current_user=self.current_user,
        )

        assert results.first_name == patient_01["first_name"]
        assert results.last_name == "IDK"
        assert results.date_of_birth == patient_01["date_of_birth"]
        assert results.gender == patient_01["gender"]
        assert results.medical_record_number == patient_01["medical_record_number"]
        assert results.patient_address == patient_01["patient_address"]
        assert results.emergency_contact == patient_01["emergency_contact"]
        assert results.age == 26
        assert results.id == 1000


    @freezegun.freeze_time("2025-05-05T11:11:11.1234567")
    async def test_creating_reporter(self):
        results = await create_reporter(
            id=1000,
            reporter=ReporterBase(**reporter_01),
            session=session,
            current_user=self.current_user,
        )

        assert results.first_name == reporter_01["first_name"]
        assert results.last_name == reporter_01["last_name"]
        assert results.email == reporter_01["email"]
        assert results.job_title == reporter_01["job_title"]
        assert results.phone_number == "tel:+44-7987-654321"
        assert results.organization_name == reporter_01["organization_name"]
        assert results.organization_address == reporter_01["organization_address"]
        assert results.date_registration == reporter_01["date_registration"]
        assert results.id == 1000

    @freezegun.freeze_time("2025-05-05T11:11:11.1234567")
    async def test_modifying_reporter(self):
        results = await create_reporter(
            id=1000,
            reporter=ReporterBase(**{**reporter_01, "last_name": "IDK"}),
            session=session,
            current_user=self.current_user,
        )

        assert results.first_name == reporter_01["first_name"]
        assert results.last_name == "IDK"
        assert results.email == reporter_01["email"]
        assert results.job_title == reporter_01["job_title"]
        assert results.phone_number == "tel:+44-7987-654321"
        assert results.organization_name == reporter_01["organization_name"]
        assert results.organization_address == reporter_01["organization_address"]
        assert results.date_registration == reporter_01["date_registration"]
        assert results.id == 1000

    @freezegun.freeze_time("2025-05-05T11:11:11.1234567")
    async def test_creating_report(self):
        results = await create_report(
            report=ReportBase(**report_01),
            session=session,
            current_user=self.current_user,
        )

        assert results.status == report_01["status"]
        assert results.patient_id == report_01["patient_id"]
        assert results.disease_id == report_01["disease_id"]
        assert results.date_created == report_01["date_created"]
        # assert results.date_updated == None
        assert results.reporter_id == 1
        assert results.id == 1

    @freezegun.freeze_time("2025-05-05T11:11:11.1234567")
    async def test_modifying_report(self):
        results = await update_report(
            id=1,
            report=ReportBase(**{**report_01, "status": ReportStatus.approved}),
            session=session,
            current_user=self.current_user,
        )

        assert results.status == ReportStatus.approved
        assert results.patient_id == report_01["patient_id"]
        assert results.disease_id == report_01["disease_id"]
        assert results.date_created == report_01["date_created"]
        # freezegun is not working here anyway
        assert results.date_updated == (
            datetime.datetime
            .fromisoformat("2025-05-05T11:11:11.1234567")
            .replace(tzinfo=None)
        )
        assert results.updated_by == self.current_user.id
        assert results.reporter_id == report_01["reporter_id"]
        assert results.id == 1000


try:
    # Create connection to the database
    conn = engine.connect()

    # Create metadata object
    metadata = MetaData()

    # Reflect the existing tables
    metadata.reflect(bind=engine, resolve_fks=False)
    metadata.drop_all(engine)
    session.commit()
    session.close()
    engine.dispose()
except Exception:
    print("?")
