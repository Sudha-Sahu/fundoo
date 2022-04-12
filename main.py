from routes import all_routes
from dotenv import load_dotenv
from db.mydatabase import user_database
from flask import Flask
import os
from flask_restful import Api

load_dotenv()

user_database()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.getenv("SECRET_KEY"))
api = Api(app)


def call_api():
    for data in all_routes:
        api_class = data[0]
        endpoint = data[1]
        api.add_resource(api_class, endpoint)


call_api()


if __name__ == "__main__":
    app.run(debug=True, port=9090)
