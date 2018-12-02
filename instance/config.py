import os

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:jamohsize@localhost/jamii_business'
