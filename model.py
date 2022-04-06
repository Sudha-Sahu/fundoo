
from mongoengine import SequenceField, BooleanField, Document, StringField, DateTimeField
import datetime


class User(Document):
    id = SequenceField(primary_key=True, required=True , null=False)
    user_name = StringField(unique=True, required=True, max_length=40)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True, min_length=5, max_length=20)
    is_active = BooleanField(default=False)
    gender = StringField(required=False)
    db_created = DateTimeField(default=datetime.datetime.now)
