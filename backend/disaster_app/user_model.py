from mongoengine import *
from datetime import datetime


class User(Document):

    name = StringField(required=True)

    email = EmailField(required=True, unique=True)

    password = StringField(required=True)

    phone = StringField()

    location = StringField()

    role = StringField(default="user")

    created_at = DateTimeField(default=datetime.now)

    meta = {
        "collection": "users"
    }