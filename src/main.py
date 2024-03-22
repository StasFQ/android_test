from typing import Annotated

from fastapi import FastAPI, Depends
from dependencies import push_notification_service
from services.push_notification import PushNotificationService
from schemas import PushNotificationCreate

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


@app.post('/notification/')
async def add_notification(push_notification_service: Annotated[PushNotificationService, Depends(push_notification_service)],
                           push_notification_data: PushNotificationCreate):
    push_notification_data_dict = push_notification_data.model_dump()
    notification_id = await push_notification_service.add_push_notification(push_notification_data_dict)
    return notification_id


@app.get('/notifications/')
async def get_notifications(push_notification_service: Annotated[PushNotificationService, Depends(push_notification_service)]):
    notifications = await push_notification_service.get_push_notifications()
    return notifications
