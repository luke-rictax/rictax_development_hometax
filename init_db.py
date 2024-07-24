from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Data, Base
import datetime

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def init_db():
    session = SessionLocal()
    # 샘플 데이터 삽입
    sample_data = [
        Data(
            date=datetime.date.today(),
            tax_month="2024-07",
            report_type="신고서종류1",
            report_class="신고구분1",
            report_category="신고유형1",
            name="상호1",
            registration_number="1234567890",
            method="접수방법1",
            timestamp="2024-07-01 10:00:00",
            receipt_number="12345",
            receipt_document="접수서류1",
            submitter_id="제출자ID1",
            attached_documents="부속서류제출여부1",
            payment_status="납부여부1"
        ),
        # 추가 샘플 데이터 삽입 가능
    ]
    session.add_all(sample_data)
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
