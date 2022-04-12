from model import UserForNotes
from mongoengine import ValidationError


def validate_username(self, username):
    exist_username = UserForNotes.objects.filter_by(user_name=username).first()
    if exist_username:
        raise ValidationError("That username already exists. Please write a different one.")


def validate_email(self, email):
    exist_email = UserForNotes.objects.filter_by(email=email).first()
    if exist_email:
        raise ValidationError("That email address belongs to different user. Please choose a different one.")


