from mongoengine import Document, StringField, SequenceField, IntField


class Label(Document):
    id = SequenceField(primary_key=True, required=True, null=False)
    label = StringField(max_length=20)
    user_id = IntField()

    def to_dict(self):
        label_data = {
            'id': self.id,
            'label': self.label,
            'user-id': self.user_id
        }
        return label_data

    def __repr__(self):
        return f"id: {self.id}, user_id : {self.user_id}"
