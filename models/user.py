from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(80), nullable=True, unique=True)
    password = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(80), nullable=False)

