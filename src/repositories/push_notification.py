from push.models import PushNotification
from utils.repository import SQLAlchemyRepository


class PushNotificationRepository(SQLAlchemyRepository):
    model = PushNotification

