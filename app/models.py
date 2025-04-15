from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import hashlib

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    events = db.relationship('Event', backref='creator', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        # Check if password is using Werkzeug's hash format
        if self.password_hash.startswith('pbkdf2:sha256:') or self.password_hash.startswith('scrypt:'):
            return check_password_hash(self.password_hash, password)
        else:
            # Assume SHA2-256 hash format used in the schema.sql
            sha2_hash = hashlib.sha256(password.encode()).hexdigest()
            return self.password_hash == sha2_hash

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade="all, delete-orphan")
    
    @property
    def registration_count(self):
        return len(self.registrations)
    
    @property
    def is_full(self):
        return self.registration_count >= self.capacity
    
    @property
    def has_started(self):
        return self.event_date <= datetime.utcnow()

class Registration(db.Model):
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    school_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow) 