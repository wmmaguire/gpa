from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from app.models.pagination import PaginatedAPIMixin
from app.models.searchable import SearchableMixin
from datetime import datetime, timedelta
from hashlib import md5
import base64
import os
import jwt
import time
from enum import IntEnum

## Privacy Enum
class PrivacyEnum(IntEnum):
    Public  = 1
    Private = 2

    ## return enum options as list
    @classmethod
    def to_list(cls):
        return [v.name for v in cls]

## Gender enum
class GenderEnum(IntEnum):
    Male    = 1
    Female  = 2
    Unknown = 3

    ## return enum options as list
    @classmethod
    def to_list(cls):
        return [v.name for v in cls]


## Model to represent user
class User(SearchableMixin, PaginatedAPIMixin, UserMixin, db.Model):
    __searchable__ = ['username']
    __tablename__ = 'user'
    # general info
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    # api key
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # personal info
    privacy  = db.Column(db.Enum(PrivacyEnum)) #enum
    gender  = db.Column(db.Enum(GenderEnum)) #enum
    about  = db.Column(db.String(140))
    dob  = db.Column(db.Date)
    credits  = db.Column(db.Float())

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    ## return user data as dict
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_active': self.last_active.isoformat() + 'Z',
            'about': self.about,
        }
        if include_email:
            data['email'] = self.email
        return data

    ## populate user info from dict data
    #  TODO:
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    ## set password. store as hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    ## verify correct password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    ## generate reset password token with expiration period
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    ## verifty password reset
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    ## generate avatar for users
    def avatar(self, size):
        # obtains icons from gravatar service.
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    ## readable user object 
    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
