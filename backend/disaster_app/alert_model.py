from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from datetime import datetime


class Alert(Document):

    title = StringField(required=True)

    description = StringField(required=True)

    location = StringField(required=True)

    severity = StringField(
        choices=["Low", "Medium", "High"],
        required=True
    )

    disaster_type = StringField(required=True)

    created_at = DateTimeField(default=datetime.now)

    meta = {
        "collection": "alerts"
    }