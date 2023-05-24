from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('LOGGED IN SUCCESSFULLY!', category='success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('INVALID PASSWORD', category='error')
        else:
            flash('EMAIL DOES NOT EXIST', category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',  methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()

        if user:
            flash('EMAIL ALREADY EXISTS', category='error')
        if len(email) < 4 :
            flash('EMAIL MUST BE GREATER THAN 4 characters.', category='error')

        elif len(first_name) < 1 :
            flash('FIRST NAME MUST BE GREATER THAN 3 characters.', category='error')

        elif password1 != password2:
            flash('PASSWORDS DON\'T MATCH', category='error')

        elif len(password1) < 7 :
            flash('PASSWORDS MUST BE AT LEAST 7 characters', category='error')

        else:
            new_user = User(email=email, first_name=first_name, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('ACCOUNT CREATED!', category='success')
            login_user(user, remember = True)

            return redirect((url_for('views.home')))

    return render_template("sign_up.html", user = current_user)
