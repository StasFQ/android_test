from pydantic import BaseModel, Field


class PushNotificationCreate(BaseModel):
    amount: float
    currency: str
    text: str

