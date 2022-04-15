from mongoengine import SequenceField, Document, StringField, DateTimeField, IntField, ReferenceField
import datetime


class Notes(Document):
    id = SequenceField(primary_key=True, required=True, null=False)
    user_id = IntField()
    title = StringField(required=True, max_length=20)
    desc = StringField(max_length=500)
    note_created = DateTimeField(required=True, default=datetime.datetime.now)

    def __repr__(self):
        return f"user_id : {self.user_id}, title: {self.title}"

    def to_dict(self):
        note_data = {"note_id": self.id,
                     "user_id": self.user_id,
                     "title": self.title,
                     "desc": self.desc,
                     "note_created": str(self.note_created)}
        return note_data
