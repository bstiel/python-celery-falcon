from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base import Base


class TimeSeries(Base):

    __tablename__ = 'timeseries'

    id = Column(UUID(as_uuid=True), primary_key=True)
    database_code = Column(String(120), unique=False, nullable=False)
    dataset_code = Column(String(120), unique=False, nullable=False)
    status = Column(String(120), unique=False, nullable=False, default='pending')
    data = Column(JSONB, nullable=True)