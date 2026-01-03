from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class JobOfferForm(FlaskForm):
    title = StringField('Titre du poste', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description du poste', validators=[DataRequired(), Length(min=20)])
    requirements = TextAreaField('Prérequis (Compétences, Diplômes...)', validators=[Length(max=500)])
    submit = SubmitField('Publier l\'offre')
