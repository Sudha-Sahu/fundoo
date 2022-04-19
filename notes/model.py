from mongoengine import SequenceField, Document, StringField, DateTimeField, IntField, ReferenceField, BooleanField, \
    ListField, PULL
import datetime
from labels import model


class Notes(Document):
    id = SequenceField(primary_key=True, required=True, null=False)
    user_id = IntField()
    title = StringField(required=True, max_length=20)
    desc = StringField(max_length=500)
    is_trash = BooleanField(default=False)
    is_pinned = BooleanField(default=False)
    color = StringField(default='black')
    label_id = ListField(ReferenceField(model.Label, reverse_delete_rule=PULL))
    note_created = DateTimeField(required=True, default=datetime.datetime.now)

    def __repr__(self):
        return f"user_id : {self.user_id}, title: {self.title}"

    def to_dict(self):
        note_data = {"note_id": self.id,
                     "user_id": self.user_id,
                     "title": self.title,
                     "desc": self.desc,
                     "is_trash": self.is_trash,
                     "is_pinned": self.is_pinned,
                     "color": self.color,
                     "label_id": [lb.label for lb in self.label_id],
                     "note_created": str(self.note_created)}
        return note_data
