from app import lm
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_socketio import Namespace, emit, ConnectionRefusedError
from flask_login import current_user
import datetime

class User(UserMixin, Document):
    username = StringField(max_length=64, required=True, unique=True)
    email = EmailField(max_length=128, required=True, unique=True)
    password_hash = StringField(max_length=192, required=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@lm.user_loader
def load_user(id):
    return User.objects(id=id).first()


class Room(Document, Namespace):
    name = StringField(max_length=64, required=True, unique=True)

    def on_connect(self, auth):
        print("Connecting to {}".format(self.name))
        if not current_user.is_authenticated:
            lm.unathorized()

    def on_disconnect(self):
        print("Disconnecting from {}".format(self.name))
        pass

    def on_my_event(self, data):
        emit('my_response', data)

    #@login_required
    def on_new_post(self, data):
        print("Posting to {}, msg: {}".format(self.name, data))
        if not current_user.is_authenticated:
            lm.unathorized()
        user = current_user
        post = Post(user=user, room=self, date=datetime.datetime.now(), msg=data)
        post.save()
        emit('feed_update', post.webview(), broadcast=True)

class Post(Document):
    user = ReferenceField('User', required=True)
    room = ReferenceField('Room', required=True)
    date = DateTimeField(required=True)
    msg = StringField(max_length=256, required=True)

    def username(self):
        return self.user.username
    
    def pretty_date(self):
        return '{:%Y-%m-%d %H:%M}'.format(self.date)

    def webview(self):
        return "{} on {} said: {}".format(self.username(), self.pretty_date(), self.msg)
    
    def as_dict(self):
        diction = {}
        diction['user'] = self.username()
        diction['date'] = self.pretty_date()
        diction['msg'] = self.msg
        return diction
        
#socketio.on_namespace(Room('/test'))
