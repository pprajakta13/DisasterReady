from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from datetime import datetime



class SOSRequest(Document):

    name = StringField(required=True)

    phone = StringField(required=True)

    location = StringField(required=True)

    pincode = StringField(required=True)

    emergency_type = StringField(required=True)

    status = StringField(default="Pending")

    created_at = DateTimeField(default=datetime.now)

    meta = {
        "collection": "sos_requests"
    }