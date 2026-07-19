from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from datetime import datetime


class Emergency(Document):

    user_name = StringField(required=True)

    email = StringField(required=True)

    location = StringField(required=True)

    emergency_type = StringField(required=True)

    status = StringField(default="Pending")

    created_at = DateTimeField(default=datetime.now)

    meta = {
        "collection": "emergencies"
    }