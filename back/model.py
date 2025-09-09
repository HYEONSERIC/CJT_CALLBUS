from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from .database import Base

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(String, primary_key=True, index=True)
    customer_type = Column(String, index=True)
    purpose = Column(String, index=True)
    step = Column(Integer, default=1)             # 진행 스텝(1=초기)
    created_at = Column(DateTime, server_default=func.now())
