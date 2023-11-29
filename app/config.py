import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:0000@localhost:5432/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
