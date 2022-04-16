from model import Label


def validate_new_label(data):
    label = data.get('label')
    user_id = data.get('user_id')
    exist_label = Label.objects.filter(user_id=user_id, label=label).first()
    if exist_label:
        return {'error': 'label name already present'}


def validate_if_label_exist(label_id):
    exist_label = Label.objects.filter(id=label_id)
    if not exist_label:
        return {'error': 'label does not exist'}

