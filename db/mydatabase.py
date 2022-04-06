from mongoengine import connect


def my_database():
    connect(host='mongodb://127.0.0.1:27017/FlaskUserProject')

