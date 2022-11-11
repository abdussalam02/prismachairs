from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Chairs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    cover = db.Column(db.String(500))
    sell_price = db.Column(db.Integer)
    disc_price = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default = func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default = func.now())
