from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.models import User, Company, Candidate
from app.auth.forms import LoginForm, RegistrationForm

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email ou mot de passe invalide', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Connexion', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit() # Commit to get user.id

        if form.role.data == 'candidate':
            candidate = Candidate(
                user_id=user.id,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.add(candidate)
        elif form.role.data == 'company':
            company = Company(
                user_id=user.id,
                name=form.company_name.data
            )
            db.session.add(company)
        
        db.session.commit()
        flash('Félicitations, vous êtes maintenant inscrit !', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Inscription', form=form)

