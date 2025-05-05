from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'))
    plan_status = db.Column(db.Boolean, default=False)
    activation_date = db.Column(db.TIMESTAMP(timezone=True))
    activation_end_date = db.Column(db.TIMESTAMP(timezone=True))
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    
    plan = db.relationship('Plan', back_populates='users')
    media = db.relationship('Media', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f'<User {self.username}>'

class Plan(db.Model):
    __tablename__ = 'plans'
    plan_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)
    activation_code = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    
    users = db.relationship('User', back_populates='plan')
    attributes = db.relationship('Attribute', back_populates='plan', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Plan {self.name}>'

class Attribute(db.Model):
    __tablename__ = 'attributes'
    attribute_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    
    plan = db.relationship('Plan', back_populates='attributes')

    def __repr__(self):
        return f'<Attribute {self.title}>'

class Media(db.Model):
    __tablename__ = 'media'
    media_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), onupdate=db.func.now())

    
    user = db.relationship('User', back_populates='media')

    __table_args__ = (
        db.CheckConstraint(type.in_(['video', 'imagen']), name='check_media_type'),
    )

    def __repr__(self):
        return f'<Media {self.media_id}>'