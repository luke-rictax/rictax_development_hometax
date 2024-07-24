from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class WithholdingTaxPayment(Base):
    __tablename__ = 'withholding_tax_payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tax_year_month = Column(String)
    report_type = Column(String)
    report_division = Column(String)
    report_category = Column(String)
    business_name = Column(String)
    registration_number = Column(String)
    reception_method = Column(String)
    reception_date = Column(String)
    reception_number = Column(String)
    reception_document = Column(String)
    receipt = Column(String)
    payment_slip = Column(String)
    submitter_id = Column(String)
    document_submission = Column(Boolean)
    payment_status = Column(Boolean)

DATABASE_URL = "sqlite:///./withholding_tax_payments.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
