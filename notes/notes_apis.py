from flask import request
from mongoengine import ValidationError
from flask_restful import Resource
import json
from .model import Notes
import datetime
from .utils import token_required
from labels.model import Label
import redis


r = redis.Redis(
    host='27017',
    port=9090,
    password='password')


class NoteAPI(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """
            This API is used to create a note for user
            @param request: It takes note-title, description, label(optional)
            @return: creates successful user notes
        """
        user_id = self.get('_id')
        data = json.loads(request.data)
        title = data.get('title')
        desc = data.get('desc')
        color = data.get('color')
        label = data.get('label')
        note_created = datetime.datetime.now()
        notes = Notes(title=title,
                      desc=desc,
                      user_id=user_id,
                      color=color,
                      note_created=note_created)
        notes.save()
        print(label)
        try:
            labl = Label.objects.filter(label=label, user_id=user_id)
            if labl:
                notes.label_id.append(labl.first())
            else:
                labl_ = Label(label=label, user_id=user_id)
                labl_.save()
                notes.label_id.append(labl_)
            notes.save()
            return {'msg': 'User added new notes', 'code': 200}
        except Exception:
            return {'error': "user not found"}

    @token_required
    def get(self, *args, **kwargs):
        """
            This API is used to fetch all notes of the user
            @return: returns all notes
        """
        user_id = self.get('_id')
        note_filter = request.args.get('filter')
        print(note_filter)
        all_notes = []

        try:
            if note_filter == 'pinned':
                my_notes = Notes.objects.filter(user_id=user_id, is_trash=False, is_pinned=True)
            elif note_filter == "trash":
                my_notes = Notes.objects.filter(user_id=user_id, is_trash=True).order_by("-is_pinned")
            else:
                my_notes = Notes.objects.filter(user_id=user_id, is_trash=False).order_by("-is_pinned")

            if not my_notes:
                return {'msg': 'NO NOTE PRESENT IN DATABASE', 'error code': 400}

            for note in my_notes:
                dict_itr = note.to_dict()
                all_notes.append(dict_itr)
        except TypeError as e:
            return {'Error': f" {e} didn't find any notes"}
        return {'notes': all_notes}


class EditNotes(Resource):
    @token_required
    def patch(self, *args, **kwargs):
        """
            This API is used to update the existing note
            @param request: title, description
            @param note_id: primary_key of the specific note
            @return: updates the note
        """
        try:
            note_id = kwargs['note_id']
            user_id = self.get('_id')
            note = Notes.objects.filter(id=note_id, user_id=user_id).first()
            updated_data = json.loads(request.data)
            note.update(**updated_data)

        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'Notes updated', 'code': 200}

    @token_required
    def delete(self, *args, **kwargs):
        """
           This API is used to delete and trash existing note
           @param note_id: primary_key of the specific note
           @return: trash or delete the note if it is already trashed
        """
        try:
            note_id = kwargs['note_id']
            user_id = self.get('_id')
            note = Notes.objects.filter(id=note_id,  user_id=user_id).first()
            if not note.is_trash:
                return {"msg": "note not found in trash"}
            if note.is_trash:
                note.delete()
                return {'message': 'Notes Deleted', 'code': 200}
        except Exception:
            return {'msg': "note not found"}

    @token_required
    def get(self, *args, **kwargs):
        """
            This API is used to fetch a notes by note id
            @param note_id: primary_key of the specific note
            @return: returns the note if it exist and belongs to the user
        """
        note_id = kwargs['note_id']
        user_id = self.get('_id')
        print(note_id, user_id)
        notes = Notes.objects.filter(id=note_id, user_id=user_id).first()
        try:
            if notes['id'] == note_id:
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'desc': notes['desc'],
                    'user_id': notes['user_id'],
                    'is_pinned': notes['is_pinned'],
                    'is_trash': notes['is_trash'],
                    'color': notes['color'],
                    'label_id': [lb.label for lb in notes.label_id],
                    'date_created': str(notes['note_created'])
                }
        except Exception:
            return {'msg': "note not found"}


class PinNotes(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """
            This API is used to pin a notes by note id
            @param note_id: primary_key of the specific note
            @return: pins the note
        """
        note_id = kwargs['note_id']
        user_id = self.get('_id')
        print(user_id, note_id)
        notes = Notes.objects.get(id=note_id)
        try:
            if not notes:
                return {'msg': 'Could not find the note', 'status code': 400}
            if notes['user_id'] == user_id:
                notes.is_pinned = True
                notes.save()
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'desc': notes['desc'],
                    'user_id': notes['user_id'],
                    'is_pinned': notes['is_pinned'],
                    'is_trash': notes['is_trash'],
                    'color': notes['color'],
                    'date_created': str(notes['note_created'])
                }
        except Exception as e:
            return {'msg': f'{e} some error occured'}


class TrashNotes(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """
            This API is used to trash a notes by note id
            @param note_id: primary_key of the specific note
            @return: trashes the note
        """
        note_id = kwargs['note_id']
        user_id = self.get('_id')
        print(user_id, note_id)
        notes = Notes.objects.get(id=note_id)
        try:
            if not notes:
                return {'msg': 'Could not find the note', 'status code': 400}
            if notes['user_id'] == user_id:
                notes.is_trash = True
                notes.save()
                return {
                    'id': notes['id'],
                    'title': notes['title'],
                    'desc': notes['desc'],
                    'user_id': notes['user_id'],
                    'is_pinned': notes['is_pinned'],
                    'is_trash': notes['is_trash'],
                    'color': notes['color'],
                    'date_created': str(notes['note_created'])
                }
        except Exception as e:
            return {'msg': f'{e} some error occured'}

