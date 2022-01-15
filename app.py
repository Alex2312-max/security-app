from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cryptography.fernet import Fernet


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_information.db'
db = SQLAlchemy(app)
PATH_TO_KEY = 'key.key'


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    speed = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<User %s>' % self.id


def preprocessing_function(data):
    assert type(data) is dict, 'Invalid type.'

    new_data = {}

    for idx_key, key in enumerate(data.keys()):
        user_info = [''.join(data[key])][0]
        new_data[key] = user_info
    return new_data


def decrypt_function(path_to_key, data):
    key = open(path_to_key, "rb").read()
    new_data = {}
    f = Fernet(key)

    for idx_key, key in enumerate(data.keys()):

        user_info = [(str(f.decrypt(bytes(element, 'utf-8')).decode("utf-8"))) for element in list(data[key])]
        new_data[key] = user_info

    return new_data


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        unorganized_info_user = decrypt_function(PATH_TO_KEY, request.json)
        print(unorganized_info_user)

        info_user = preprocessing_function(unorganized_info_user)
        user_name = info_user['user_name']
        last_name = info_user['last_name']
        email = info_user['email']
        speed = float(info_user['speed'])
        new_user = Data(user_name=user_name, last_name=last_name, email=email, speed=speed)

        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return 'Invalid information provided.'
        return 'User registered'


if __name__ == '__main__':
    app.run(debug=True)
