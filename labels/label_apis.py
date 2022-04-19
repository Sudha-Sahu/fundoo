from flask import request
from flask_restful import Resource
import json
from .model import Label
from .utils import token_required


class LabelAPI(Resource):
    @token_required
    def post(self, *args, **kwargs):
        """
        This api is for creating new label.
        :param args:
        :param kwargs:
        :return: it returns all the labels of particular user
        """
        user_id = self.get('_id')
        data = json.loads(request.data)
        label = data.get('label')
        label_data = Label(label=label, user_id=user_id)
        print(label_data)
        label_data.save()
        try:
            if label_data:
                return {'message': 'label added', 'code': 200}
        except:
            return {'message': "user mot found"}

    @token_required
    def get(self, *args, **kwargs):
        """
        This api is for returning all the labels of that user stored in the database,
        :param args:
        :param kwargs:
        :return: it returns all the labels of particular user
        """
        try:
            user_id = self.get('_id')
            my_label = Label.objects.filter(user_id=user_id)
            if not my_label:
                return {'msg': 'NO LABEL PRESENT IN DATABASE', 'error code': 400}
            all_label = []
            for each_label in my_label:
                dict_itr = each_label.to_dict()
                all_label.append(dict_itr)
            print(all_label)
        except Exception as e:
            return {'Error': f" {e} didn't find any label"}
        return {'notes': all_label}


class EditLabel(Resource):
    @token_required
    def patch(self, *args, **kwargs):
        """
        This api is for updating the labels of that user stored in the database,
        :param args:
        :param kwargs:
        :return: label updated message
        """
        try:
            user_id = self.get('_id')
            label_id = kwargs['label_id']
            print(user_id, label_id)
            label = Label.objects.filter(id=label_id).first()
            updated_data = json.loads(request.data)
            label.update(**updated_data)

        except Exception as e:
            return {'Error': str(e), 'code': 500}
        return {'message': 'label updated', 'code': 200}

    @token_required
    def delete(self, *args, **kwargs):
        """
        This api is for deleting the labels of that user stored in the database,
        :param args:
        :param kwargs:
        :return: label delete message
        """
        try:
            user_id = self.get('_id')
            label_id = kwargs['label_id']
            label = Label.objects.filter(id=label_id, user_id=user_id).first()
            if label:
                label.delete()
            return {'message': 'Label Deleted', 'code': 200}
        except Exception:
            return {'msg': "label not found"}

    @token_required
    def get(self, *args, **kwargs):
        """
        This api get the label of that user using user id and label id
        :param args:
        :param kwargs:
        :return: returns the label
        """
        user_id = self.get('_id')
        label_id = kwargs['label_id']
        label = Label.objects.filter(id=label_id, user_id=user_id).first()
        try:
            if label['id'] == label_id:
                return {
                    'id': label['id'],
                    'label': label['label'],
                    'user_id': label['user_id']
                }
        except Exception:
            return {'msg': "label not found"}
