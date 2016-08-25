

from . import app, redis
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    openid = db.Column(db.String(32), primary_key=True, index=True)
    last_dialog_dt = db.Column(db.DateTime, default=None)
    subscribe_dt = db.Column(db.DateTime, default=None)
    message = db.relationship('Message', backref='user')

    def __repr__(self):
        return '<openid %r>' % self.openid

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(32), db.ForeignKey('users.openid'))
    message_type = db.Column(db.String(16), nullable=False)
    message_content = db.Column(db.Text)
    dt = db.Column(db.DateTime)

    def __repr__(self):
        return '<message %s>' % self.message_content[:10]

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

def user_to_redis(openid, datatime=None):
    redis.hmset('wechat:openid:%s', 'openid', openid, 'datatime', datatime)

