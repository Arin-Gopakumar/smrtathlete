from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                category='success'
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again!", category='error')
        else:
            flash("Email does not exist!", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash("Password must be greater than 6 characters.", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            # Use the new_user object here, not the user object from the query
            login_user(new_user, remember=True)

            category='success'
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/concussion')
@login_required
def concussions():
    return render_template('concussion.html', user=current_user)

@auth.route('/concussion-exam')
@login_required
def concussionExam():
    return render_template('concussion-exam.html', user=current_user)

@auth.route('/our-team')
@login_required
def ourTeam():
    return render_template('our-team.html', user=current_user)

@auth.route('/concussion-faq')
@login_required
def concussionFaq():
    return render_template('concussion-faq.html', user=current_user)

@auth.route('/contact-us')
@login_required
def connect():
    return render_template('contact-us.html', user=current_user)

@auth.route('/result')
@login_required
def result():
    # Retrieve the user's concussion score from the session (if stored)
    user_score = session.get('userScore')
    session.pop('userScore', None)  # Clear the stored score to avoid showing it on page refresh

    return render_template('result.html', user_score=user_score, user=current_user)

