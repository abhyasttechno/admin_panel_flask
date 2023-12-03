# password context for encrypting password using cryptography
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.context import CryptContext

db = SQLAlchemy()

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)




class LoginUser(db.Model):
    __tablename__ = 'tbl_login_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    pass_word = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(500), nullable=True)
    user_status = db.Column(db.String(50), nullable=True)
    dt_time = db.Column(db.DateTime, nullable=True)

