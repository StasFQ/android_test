from repositories.push_notification import PushNotificationRepository
from services.push_notification import PushNotificationService


def push_notification_service():
    return PushNotificationService(PushNotificationRepository)
