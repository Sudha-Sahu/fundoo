from flask import request, session
from mongoengine import ValidationError
from flask_restful import Resource
import json
from fundoo.user import model
from .model import Notes
import datetime
from .validators import validate_new_note
from .utils import get_token, decoded_token, token_required


class Note(Resource):
    @token_required
    def post(self):
        req_data = request.data
        note_data = json.loads(req_data)
        try:
            note_id = note_data.get('id')
            topic = note_data.get('topic')
            note_body = note_data.get('note_body')
            note_created = datetime.datetime.now()
            data_validate = validate_new_note(note_data)
            if data_validate:
                return data_validate
            new_note = Notes(id=note_id, topic=topic, note_body=note_body, note_created=note_created)
            new_note.save()
            print(new_note)
        except Exception:
            return {'Error': "something went wrong", 'code': 505}

        return {'msg': 'User added new notes', 'code': 200}

    @token_required
    def get(self):
        req_data = request.data
        note = json.loads(req_data)
        try:
            note['user_id'] = session['user_id']
            my_notes = Notes.objects.filter(user_id=note['user_id']).first()
            if not my_notes:
                return {'msg': 'Something went wrong', 'error code': 400}
            all_notes = []
            for note in my_notes:
                dict_itr = note.to_dict()
                all_notes.append(dict_itr)
            print(all_notes)
        except Exception as e:
            return {'Error': "didn't find any notes"}

        return {'notes': all_notes}


class EditNotes(Resource):
    @token_required
    def patch(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id, user_id=session['user_id']).first()
            new_body = request.form.get('note_body')
            note.update(note_body=new_body)
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Notes updated', 'code': 200}

    @token_required
    def delete(self, note_id):
        try:
            note = Notes.objects.filter(id=note_id,  user_id=session['user_id']).first()
            if note:
                note.delete()
            return {'message': 'Notes Deleted', 'code': 200}
        except Exception:
            return {'msg': "note not found"}

    @token_required
    def get(self, note_id):
        notes = Notes.objects.get(id=note_id).first()
        try:
            if notes:
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'note_body': notes['note_body'],
                    'user_id': notes['user_id'],
                    'user_name': notes['user_name'],
                    'date_created': str(notes['date_created'])
                }
        except Exception:
            return {'msg': "note not found"}
