from app import db, lm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_socketio import Namespace, emit, ConnectionRefusedError
from flask_login import current_user
import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Room(Namespace, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

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
        #emit('after connect',  {'data':'Lets dance'})
        user = current_user
        #db.session.execute(db.select(Room).filter_by(name=name)).scalar_one_or_none()
        post = Post(user_id=user.id, room_id=self.id, date=datetime.datetime.now(), msg=data)
        db.session.add(post)
        db.session.commit()
        emit('feed_update', post.webview(), broadcast=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    msg = db.Column(db.String(256), nullable=False)

    def username(self):
        return db.session.execute(db.select(User).filter_by(id=self.user_id)).scalar_one().username
    
    def pretty_date(self):
        return '{:%Y-%m-%d %H:%M}'.format(self.date)

    def webview(self):
        #user = User.query.filter_by(username=form.username.data).first()
        return "{} on {} said: {}".format(self.username(), self.pretty_date(), self.msg)
    
    def as_dict(self):
        diction = {}
        diction['user'] = self.username()
        diction['date'] = self.pretty_date()
        diction['msg'] = self.msg
        return diction
        
#socketio.on_namespace(Room('/test'))
