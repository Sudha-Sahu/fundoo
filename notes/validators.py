

def validate_new_note(data):
    topic = data.get('topic')
    body = data.get('body')
    if not body or not topic:
        return {'Error': 'body and topic are required fields'}


