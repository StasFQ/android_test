from fastapi import HTTPException


class PushNotificationService:
    def __init__(self, push_notification_repository):
        self.push_notification_repository = push_notification_repository()

    async def add_push_notification(self, push_notification_dict):
        try:
            notification_id = await self.push_notification_repository.add_one(push_notification_dict)
            return notification_id
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'{e}')

    async def get_push_notifications(self):
        try:
            notifications = await self.push_notification_repository.find_all()
            return notifications
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'{e}')
