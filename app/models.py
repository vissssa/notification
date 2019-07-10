"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""
from datetime import datetime

from .extenions import db


class Mixin(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class Message(Mixin):
    UNREAD = 0
    READ = 1
    DISABLE = 2

    rec_id = db.Column(db.Integer)
    content_id = db.Column(db.Integer)
    status = db.Column(db.Integer)


class Content(Mixin):
    PRIVATE = 0
    PUBLIC = 1
    GLOBAL = 2

    send_id = db.Column(db.Integer)
    content = db.Column(db.String(200))
    type = db.Column(db.Integer)
    group = db.Column(db.String(20))
    create_time = db.Column(db.DateTime, default=datetime.now)
