from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if len(name) < 3:
            flash("Name should be greater than 3 characters", category='error')
        elif len(email) < 6:
            flash("Email should be greater than 6 character including @gmail.com", category='error')
        elif len(phone) < 8:
            flash("Phone should be greater than 8 Number", category='error')
        elif len(password) < 8:
            flash("Password should be greater than 8 character", category='error')
        elif password != password2:
            flash("Password and Confirm Password doesn't match", category='error')
        else:
            user = User(name=name, email=email, phone=phone, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully", category='success')

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.is_admin:
                    login_user(user, remember=True)
                    flash(f"You are successfully logged in Mr. {user.name}", category='success')
                    return redirect(url_for('views.admin'))
                else:
                    flash("You are not an admin yet, so you cannot access admin panel")
            else:
                flash(f"Wrong password {user.name}, Try again!", category='error')
        else:
            flash("You do not have an account please create one and wait for verification", category='error')
            return redirect(url_for('auth.register'))

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("User logged out successfully")
    return redirect(url_for('auth.login'))