from datetime import datetime, timedelta
import sqlalchemy
import os
import base64
from . import db_session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(db_session.SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    public_id = sqlalchemy.Column(sqlalchemy.String, unique=True)

    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
    admin = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)

    token = sqlalchemy.Column(sqlalchemy.String(32), index=True, unique=True)
    token_expiration = sqlalchemy.Column(sqlalchemy.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db_sess = db_session.create_session()
        db_sess.add(self)
        db_sess.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.token == token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def __repr__(self):
        return f"<{self.__tablename__}>\t{self.name}\t{self.email}"
