from mongoengine import *
from datetime import datetime


class Notification(Document):

    title = StringField(required=True)

    message = StringField(required=True)

    created_at = DateTimeField(default=datetime.now)

    read = BooleanField(default=False)

    meta = {
        "collection": "notifications"
    }