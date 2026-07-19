from mongoengine import Document
from mongoengine import StringField
from mongoengine import BooleanField


class Checklist(Document):

    item = StringField(required=True)

    completed = BooleanField(default=False)

    category = StringField(required=True)

    meta = {
        "collection": "checklists"
    }
    