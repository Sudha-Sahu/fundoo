from flask import request
from mongoengine import ValidationError
from flask_restful import Resource
import json
from model import Label
from utils import token_required
from validators import validate_new_label


class LabelAPI(Resource):
    @token_required
    def post(self, *args, **kwargs):
        try:
            user_id = self.get('_id')
            data = json.loads(request.data)
            label = data.get('label')
            label_data = Label.objects.filter(user_id=user_id, label=label).first()
            if label_data:
                return {'data': label_data, 'code': 500}
            label_data.save()
            return {'message': 'label added', 'code': 200}

        except ValidationError:
            return {'error': "user not found"}

    @token_required
    def get(self, *args, **kwargs):
        user_id = self.get('_id')
        try:
            my_label = Label.objects.filter(user_id=user_id)
            if not my_label:
                return {'msg': 'NO LABEL PRESENT IN DATABASE', 'error code': 400}
            all_label = []
            for lb in my_label:
                dict_itr = lb.to_dict()
                all_label.append(dict_itr)
            print(all_label)
        except Exception as e:
            return {'Error': f" {e} didn't find any label"}
        return {'notes': all_label}


class EditLabel(Resource):
    @token_required
    def delete(self, *args, **kwargs):
        try:
            label_id = kwargs['label_id']
            user_id = self.get('_id')
            label = Label.objects.filter(id=label_id,  user_id=user_id).first()
            if label:
                label.delete()
            return {'message': 'Label Deleted', 'code': 200}
        except Exception:
            return {'msg': "label not found"}

    @token_required
    def get(self, *args, **kwargs):
        label_id = kwargs['label_id']
        user_id = self.get('_id')
        label = Label.objects.filter(id=label_id, user_id=user_id).first()
        try:
            if label['id'] == label_id:
                return {
                    'id': label['id'],
                    'user_id': label['user_id'],
                    'label': label['label'],
                }
        except Exception:
            return {'msg': "label not found"}
