from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class CVUploadForm(FlaskForm):
    cv = FileField('Télécharger votre CV (PDF ou DOCX)', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'docx'], 'Seuls les fichiers PDF et DOCX sont autorisés.')
    ])
    submit = SubmitField('Analyser')
