from .model import Notes
from mongoengine import ValidationError


def validate_new_note(data):
    topic = data.get('topic')
    body = data.get('body')
    if not body or not topic:
        return {'Error': 'body and topic are required fields'}




"""
def validate_username(username):
    exist_username = UserForNotes.objects.filter_by(user_name=username).first()
    if exist_username:
        raise ValidationError("That username already exists. Please write a different one.")


def validate_email(email):
    exist_email = UserForNotes.objects.filter_by(email=email).first()
    if exist_email:
        raise ValidationError("That email address belongs to different user. Please choose a different one.")
"""

