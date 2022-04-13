from mongoengine import SequenceField, Document, StringField, DateTimeField, IntField, ReferenceField
import datetime
from fundoo.user.model import User


class Notes(Document):
    id = SequenceField(primary_key=True, required=True, null=False)
    user_id = IntField(ReferenceField(User))
    user_name = StringField(max_length=50)
    title = StringField(required=True, max_length=20)
    note_body = StringField(max_length=100)
    note_created = DateTimeField(required=True, default=datetime.datetime.now)
