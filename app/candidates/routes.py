import os
import json
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.candidates import bp
from app.candidates.forms import CVUploadForm
from app.models import Candidate
from app.nlp.extraction import extract_text_from_pdf, extract_text_from_docx
from app.nlp.preprocessing import preprocess_cv

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'candidate':
        flash('Accès réservé aux candidats.', 'warning')
        return redirect(url_for('main.index'))
    
    candidate = current_user.candidate_profile
    if not candidate:
        # Should not happen if registration works correctly, but safety check
        candidate = Candidate(user_id=current_user.id, first_name="", last_name="")
        db.session.add(candidate)
        db.session.commit()

    form = CVUploadForm()
    if form.validate_on_submit():
        f = form.cv.data
        filename = secure_filename(f.filename)
        
        # Ensure upload directory exists
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])
            
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        
        # Extract text
        text = ""
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        elif filename.lower().endswith('.docx'):
            text = extract_text_from_docx(filepath)
            
        if text:
            # Analyze CV
            analysis = preprocess_cv(text)
            
            # Update Candidate Profile
            candidate.cv_path = filename
            candidate.skills = json.dumps(analysis.get('skills', []))
            candidate.education = json.dumps(analysis.get('education', []))
            # Experience extraction is tricky, for now we might store entities or raw text
            # The current NLP module doesn't have specific experience extraction logic beyond entities
            candidate.experience = json.dumps(analysis.get('entities', {})) 
            
            db.session.commit()
            flash('CV analysé avec succès !', 'success')
        else:
            flash('Impossible d\'extraire le texte du fichier.', 'danger')
            
        return redirect(url_for('candidates.profile'))

    return render_template('candidates/profile.html', form=form, candidate=candidate)

