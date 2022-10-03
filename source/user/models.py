from source.models.base_model import BaseModel
from source import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from source import login_manager


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24))
    email = db.Column(db.String(48))
    password = db.Column(db.String(48))
    experience = db.Column(db.String(24))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, username, email, password_hash, experience, role_id):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password_hash)
        self.experience = experience
        self.role_id = role_id

    def __repr__(self):
        return f"User: {self.username}"

    def check_password(self, login_password):
        return check_password_hash(self.password, login_password)

    @classmethod
    def find_by_email(cls, temp_email):
        email = cls.query.filter_by(email=temp_email).first()
        if email:
            return email

    def is_admin(self):
        return self.role == "admin"

    def has_roles(self, *args):
        return set(args).issubset({role.name for role in self.role})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Role(db.Model):

    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return self.name


class Item(BaseModel):
    __tablename__ = 'item'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    ingredients = db.Column(db.String())
    creator = db.Column(db.String())

    def __init__(self, name, ingredients, creator):
        self.name = name
        self.ingredients = ingredients
        self.creator = creator

    def __repr__(self):
        return f'ID: {self.id} Name: {self.name} Creator: {self.creator} Ingredients: {self.ingredients}'


class ItemUsers(BaseModel):

    __tablename__ = 'item_users'

    id = db.Column(db.Integer(), primary_key=True)
    creator_id = db.Column(db.Integer())
    item_id = db.Column(db.Integer())


class Creator(BaseModel):

    __tableName__ = 'creator'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(48))
    email = db.Column(db.String(48))
    drinks = db.Column(db.String(400))

    def __init__(self, name, email, drinks):
        self.name = name
        self.email = email
        self.drinks = drinks

    def __repr__(self):
        return f'Name: {self.name} Email: {self.email} Creations: {self.drinks}'


class Venue(BaseModel):

    __tableName__ = 'venue'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(48))
    email = db.Column(db.String(48))
    location = db.Column(db.String(96))
    tags = db.Column(db.String(400))

    def __init__(self, name, email, location, tags):
        self.name = name
        self.email = email
        self.location = location
        self.tags = tags

    def __repr__(self):
        return f'Name: {self.name} Email: {self.email} Location: {self.location} Tags: {self.tags}'



