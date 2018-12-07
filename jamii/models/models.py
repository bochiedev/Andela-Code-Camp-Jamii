from datetime import datetime
from jamii import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    business = db.relationship('Business', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.image_file}')"


class Businesscategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Businesscategory('{self.name}')"


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey(
        'businesscategory.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Business('{self.name}, {self.owner}, {self.location}')"

class BusinessReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    business = db.Column(db.Integer, db.ForeignKey(
                    'business.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"BusinessReviews('{self.name}, {self.message}')"
