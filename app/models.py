import json
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False) # 'company' or 'candidate'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company_profile = db.relationship('Company', backref='user', uselist=False)
    candidate_profile = db.relationship('Candidate', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    jobs = db.relationship('JobOffer', backref='company', lazy=True)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cv_path = db.Column(db.String(200))
    skills = db.Column(db.Text) # Stored as JSON string or comma-separated
    experience = db.Column(db.Text) # Stored as JSON string
    education = db.Column(db.Text) # Stored as JSON string
    applications = db.relationship('Application', backref='candidate', lazy=True)

    def get_skills_list(self):
        if self.skills:
            try:
                return json.loads(self.skills)
            except:
                return []
        return []

    def get_education_list(self):
        if self.education:
            try:
                return json.loads(self.education)
            except:
                return []
        return []

class JobOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    skills = db.Column(db.Text) # Stored as JSON string
    education = db.Column(db.Text) # Stored as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('Application', backref='job', lazy=True)

    def get_skills_list(self):
        if self.skills:
            try:
                return json.loads(self.skills)
            except:
                return []
        return []


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_offer.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, accepted, rejected
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
