# place for authorization
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
# the idea is you never store the password in plain text, and if you hash the password, you can never return to the original password, you
# can only check the password you type in is correct or equal to the hast that it stored.
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=[
    'GET',
    'POST'
])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email does not exist!', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # return "<p> log out </p>"
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=[
    'GET',
    'POST'
])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already been used', category='error')
        elif len(email) < 4:
            flash('Email not valid', category='error')
        elif len(first_name) <= 2:
            flash('First name not valid', category='error')
        elif password1 != password2:
            flash('password not same', category='error')
        elif len(password1) < 7: 
            flash('password not valid', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('created', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
