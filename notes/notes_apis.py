from flask import request, session
from mongoengine import ValidationError
from flask_restful import Resource
import json
from .model import Notes
import datetime
from .utils import token_required
from .validators import validate_new_note


class NoteAPI(Resource):
    @token_required
    def post(self, *args, **kwargs):
        try:
            user_id = self.get('_id')
            data = json.loads(request.data)
            title = data.get('title')
            desc = data.get('desc')
            note_created = datetime.datetime.now()
            notes = Notes(title=title, desc=desc, user_id=user_id, note_created=note_created)
            notes.save()
            return {'msg': 'User added new notes', 'code': 200}
        except Exception:
            return {'error': "user not found"}

    @token_required
    def get(self, *args, **kwargs):
        user_id = self.get('_id')
        try:
            my_notes = Notes.objects.filter(user_id=user_id)
            if not my_notes:
                return {'msg': 'NO NOTE PRESENT IN DATABASE', 'error code': 400}
            all_notes = []
            for note in my_notes:
                dict_itr = note.to_dict()
                all_notes.append(dict_itr)
            print(all_notes)
        except Exception as e:
            return {'Error': f" {e} didn't find any notes"}

        return {'notes': all_notes}


class EditNotes(Resource):
    @token_required
    def patch(self, *args, **kwargs):
        try:
            note_id = kwargs['note_id']
            user_id = self.get('_id')
            note = Notes.objects.filter(id=note_id, user_id=user_id).first()
            updated_data = request.form
            note.update(**updated_data)
        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Notes updated', 'code': 200}

    @token_required
    def delete(self, *args, **kwargs):
        try:
            note_id = kwargs['note_id']
            user_id = self.get('_id')
            note = Notes.objects.filter(id=note_id,  user_id=user_id).first()
            if note:
                note.delete()
            return {'message': 'Notes Deleted', 'code': 200}
        except Exception:
            return {'msg': "note not found"}

    @token_required
    def get(self, *args, **kwargs):
        note_id = kwargs['note_id']
        user_id = self.get('_id')
        notes = Notes.objects.filter(id=note_id, user_id=user_id).first()
        try:
            if notes['id'] == note_id:
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'desc': notes['desc'],
                    'user_id': notes['user_id'],
                    'date_created': str(notes['note_created'])
                }
        except Exception:
            return {'msg': "note not found"}
