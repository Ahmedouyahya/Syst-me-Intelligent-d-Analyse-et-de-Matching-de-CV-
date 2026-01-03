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
    first_name = StringField('Prénom', validators=[Length(min=2, max=50)])
    last_name = StringField('Nom', validators=[Length(min=2, max=50)])
    
    # Fields for Company
    company_name = StringField('Nom de l\'entreprise', validators=[Length(min=2, max=100)])
    
    submit = SubmitField('S\'inscrire')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')
