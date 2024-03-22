from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, TIMESTAMP, Float, DateTime, func, \
    Enum
from database import Base
from datetime import datetime


class PushNotification(Base):
    __tablename__ = 'push_notifications'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    currency = Column(String)
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
