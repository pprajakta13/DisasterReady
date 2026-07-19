from mongoengine import Document
from mongoengine import StringField


class Resource(Document):

    name = StringField(required=True)

    resource_type = StringField(required=True)

    address = StringField(required=True)

    contact = StringField(required=True)

    meta = {
        "collection": "resources"
    }