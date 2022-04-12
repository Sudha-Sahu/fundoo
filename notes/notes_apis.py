from flask import request
from mongoengine import ValidationError
from flask_restful import Resource
import json
from model import UserForNotes, Notes
import datetime


class RegistrationForNotes(Resource):
    def post(self):
        data = json.loads(request.data)
        user_name = data.get('user_name')
        password = data.get('password')
        conf_password = data.get('conf_password')
        email = data.get('email')
        if conf_password != password:
            return {'error': 'password did not matched'}
        try:
            new_user = UserForNotes(user_name=user_name, password=password, email=email)
            new_user.save()
        except ValidationError as e:
            return {'error': e.to_dict()}
        return {'msg': 'new user added successfully for keeping notes'}


class LoginForNotes(Resource):
    def get(self):
        try:
            data = request.args
            user_name = data.get('user_name')
            password = data.get('password')
            user = UserForNotes.objects.get(user_name=user_name)
            token = None
            if not user:
                return {'error': 'user not found'}
            if password != user.password:
                return {'error': 'password not matching'}
            user.save()
            return {'msg': 'you are logged in....'}
        except Exception:
            return {'error': 'some error occured Please login again', 'status code': 400}


class AddNewNote(Resource):
    def post(self):
        data = json.loads(request.data)
        note_id = data.get('id')
        title = data.get('title')
        body = data.get('note_body')
        note_created = datetime.datetime.now()
        try:
            new_note = Notes(id=note_id, title=title, note_body=body, note_created=note_created)
            new_note.save()
        except Exception as e:
            return {'error': f"{e} write again your note"}
        return {'msg': 'successfully user added notes'}


class EditNote(Resource):
    def post(self):
        try:
            data = json.loads(request.data)
            note_id = data.get('id')
            new_id = Notes.objects.get(id=note_id)
            if not new_id:
                return {"msg": "note not found that you want to edit"}
            new_id.title = data.get('title')
            new_id.note_body = data.get('note_body')
            new_id.save()
            return {"msg": "user has edited and update the note"}
        except Exception:
            return {'msg': "note id is not valid"}


class DeleteNote(Resource):
    def get(self):
        note_id = request.form.get('user_id')
        data = Notes.objects(id=note_id).first()
        if not data:
            return {'message': 'note id not found!!'}
        data.deleteOne(id=note_id)
        data.save()
        return {'msg': "user note has deleted!!!"}

