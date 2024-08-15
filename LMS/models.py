from datetime import datetime
from LMS import db, login_manager
from flask_login import UserMixin
from sqlalchemy import CheckConstraint

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.Integer, nullable=False, default=1) 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Faculty(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    designation = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(50), nullable=False)
    cabin = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.String(3), nullable=False)
    remark = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.Integer, nullable=False, default=0)  

    def __init__(self, name, designation, cabin, availability, remark, password, school):
        self.name = name
        self.designation = designation
        self.school = school
        self.cabin = cabin
        self.availability = availability
        self.remark = remark
        self.password = password

    def __repr__(self):
        return f"Faculty(name='{self.name}', designation='{self.designation}', school='{self.school}', cabin='{self.cabin}', availability='{self.availability}', remark='{self.remark}', user_type='{self.type}')"



