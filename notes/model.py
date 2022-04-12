from mongoengine import SequenceField, Document, StringField, DateTimeField, IntField
import datetime


class Notes(Document):
    id = SequenceField(primary_key=True, required=True, null=False)
    user_id = IntField()
    user_name = StringField(max_length=50)
    title = StringField(required=True, max_length=20)
    note_body = StringField(max_length=100)
    note_created = DateTimeField(required=True, default=datetime.datetime.now)


class UserForNotes(Document):
    id = SequenceField(primary_key=True, required=True , null=False)
    user_name = StringField(unique=True, required=True, max_length=40)
    email = StringField(required=True)
    password = StringField(required=True, min_length=5, max_length=20)

