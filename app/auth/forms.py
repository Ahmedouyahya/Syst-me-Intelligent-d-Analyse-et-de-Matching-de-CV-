from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Je suis un(e)', choices=[('candidate', 'Candidat'), ('company', 'Entreprise')], validators=[DataRequired()])
    
    # Fields for Candidate
    first_name = StringField('Prénom')
    last_name = StringField('Nom')
    
    # Fields for Company
    company_name = StringField('Nom de l\'entreprise')
    
    submit = SubmitField('S\'inscrire')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')

    def validate_first_name(self, first_name):
        if self.role.data == 'candidate':
            if not first_name.data or len(first_name.data) < 2:
                raise ValidationError('Le prénom doit contenir au moins 2 caractères.')
            if len(first_name.data) > 50:
                raise ValidationError('Le prénom ne doit pas dépasser 50 caractères.')

    def validate_last_name(self, last_name):
        if self.role.data == 'candidate':
            if not last_name.data or len(last_name.data) < 2:
                raise ValidationError('Le nom doit contenir au moins 2 caractères.')
            if len(last_name.data) > 50:
                raise ValidationError('Le nom ne doit pas dépasser 50 caractères.')

    def validate_company_name(self, company_name):
        if self.role.data == 'company':
            if not company_name.data or len(company_name.data) < 2:
                raise ValidationError('Le nom de l\'entreprise doit contenir au moins 2 caractères.')
            if len(company_name.data) > 100:
                raise ValidationError('Le nom de l\'entreprise ne doit pas dépasser 100 caractères.')
