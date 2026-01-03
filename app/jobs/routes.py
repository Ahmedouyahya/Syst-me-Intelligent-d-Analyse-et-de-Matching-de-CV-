import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.jobs import bp
from app.jobs.forms import JobOfferForm
from app.models import JobOffer, Company, Candidate
from app.nlp.preprocessing import preprocess_job_description
from app.nlp.matching import match_profile

@bp.route('/')
def list_jobs():
    jobs = JobOffer.query.order_by(JobOffer.created_at.desc()).all()
    
    # If candidate, calculate match scores
    recommendations = []
    if current_user.is_authenticated and current_user.role == 'candidate' and current_user.candidate_profile:
        candidate = current_user.candidate_profile
        if candidate.skills: # Only if candidate has a profile with skills
            cv_data = {
                "skills": candidate.get_skills_list(),
                "education": candidate.get_education_list(),
                "cleaned_text": "" # We might need to store cleaned text in DB or re-extract
            }
            # Note: We are missing the full text for text similarity if we don't store it.
            # For now, we'll rely on skills and education.
            
            for job in jobs:
                job_data = {
                    "required_skills": job.get_skills_list(),
                    "required_education": json.loads(job.education) if job.education else [],
                    "cleaned_text": job.description # Use description as proxy
                }
                
                # We need to handle the case where cleaned_text is missing for candidate
                # For better results, we should store cleaned_text in Candidate model
                # For now, let's assume 0 text similarity if missing
                
                match_result = match_profile(cv_data, job_data)
                recommendations.append({
                    "job": job,
                    "score": match_result['total_score'],
                    "details": match_result
                })
            
            # Sort by score
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return render_template('jobs/recommendations.html', recommendations=recommendations)

    return render_template('jobs/list.html', jobs=jobs)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_job():
    if current_user.role != 'company':
        flash('Seules les entreprises peuvent publier des offres.', 'warning')
        return redirect(url_for('main.index'))
    
    # Ensure company profile exists
    if not current_user.company_profile:
        company = Company(user_id=current_user.id, name="Ma Société") # Placeholder name
        db.session.add(company)
        db.session.commit()

    form = JobOfferForm()
    if form.validate_on_submit():
        # Analyze Job Description
        analysis = preprocess_job_description(form.description.data + " " + form.requirements.data)
        
        job = JobOffer(
            title=form.title.data,
            description=form.description.data,
            requirements=form.requirements.data,
            company_id=current_user.company_profile.id,
            skills=json.dumps(analysis.get('required_skills', [])),
            education=json.dumps(analysis.get('required_education', []))
        )
        db.session.add(job)
        db.session.commit()
        flash('Offre publiée avec succès !', 'success')
        return redirect(url_for('jobs.list_jobs'))
    
    return render_template('jobs/create.html', form=form)

@bp.route('/<int:job_id>/candidates')
@login_required
def job_candidates(job_id):
    job = JobOffer.query.get_or_404(job_id)
    
    # Ensure user is the owner of the job
    if current_user.role != 'company' or job.company_id != current_user.company_profile.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('jobs.list_jobs'))
    
    candidates = Candidate.query.all()
    recommendations = []
    
    job_data = {
        "required_skills": job.get_skills_list(),
        "required_education": json.loads(job.education) if job.education else [],
        "cleaned_text": job.description
    }
    
    for candidate in candidates:
        if candidate.skills:
            cv_data = {
                "skills": candidate.get_skills_list(),
                "education": candidate.get_education_list(),
                "cleaned_text": "" # Missing full text storage for candidate
            }
            
            match_result = match_profile(cv_data, job_data)
            recommendations.append({
                "candidate": candidate,
                "score": match_result['total_score'],
                "details": match_result
            })
    
    # Sort by score
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('jobs/candidates.html', job=job, recommendations=recommendations)



