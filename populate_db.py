from datetime import datetime as dt
from os import getenv
from sqlmodel import Session, SQLModel, create_engine

from src.tests.data.db_test_data import diseases, patients, reporters, reports
from src.models import (Disease, Patient, Reporter, Report)

DB_URL = getenv("DB_URL")

engine = create_engine(DB_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def populate():
    with Session(engine) as session:
        try:
            for model, entities in (
                (Disease, diseases),
                (Patient, patients),
                (Reporter, reporters),
                (Report, reports),
            ):
                for entity in entities:
                    entity = {
                        k: (dt.fromisoformat(v) if k.startswith("date_") and v else v)
                        for k, v in entity.items()
                    }
                    session.add(model(
                        **entity,
                    ))
                    # session.commit()

            session.commit()
        except Exception:
            session.rollback()
            raise
        else:
            print("All done!")


if __name__ == "__main__":
    create_db_and_tables()
    populate()
