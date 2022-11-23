from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Chairs, Contact
from . import db
import os

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/chairs/'
ALLOWED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

@views.route('/')
def home():
    data = Chairs.query.all()
    return render_template('index.html', chairs = data)

@views.route('/message', methods=['POST'])
def message():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')

        db.session.add(Contact(name=name, number=phone, email=email, message=message))
        db.session.commit()
        flash("We have received your message we will get back to you really soon.", category='success')
    return redirect(url_for('views.home'))


@views.route('/msgview', methods=['GET', 'POST'])
def msgview():
    data = Contact.query.all()
    return render_template('contact.html', msgdata=data, user=current_user)

@views.route('/delmsg/<id>/', methods=['GET', 'POST'])
@login_required
def delmsg(id):
    data = Contact.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("Message Deleted Successfully", category='success')
    return redirect(url_for('views.msgview'))


@views.route('/chair')
def chair():
    data = Chairs.query.all()
    return render_template('chair.html', chairs=data)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    data = Chairs.query.all()
    return render_template('admin.html', chairs=data, user=current_user)

@views.route('/insert', methods=['GET', 'POST'])
@login_required
def insert():
    if request.method == 'POST':
        title = request.form.get('title')

        if 'cover' not in request.files:
            flash("No file in form", category='error')
            return redirect(request.url)

        file = request.files['cover']
        desc = request.form.get('description')
        
        if file.filename == '':
            flash("No file selected", category='error')
            return redirect(request.url)
        else:
            _ , b = os.path.splitext(secure_filename(file.filename))
            if b.lower() in ALLOWED_FORMATS:
                filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(filename)
                db.session.add(Chairs(title=title, cover=filename[8:], description=desc))
                db.session.commit()
                flash("Chair Added Successfully", category='success')
            else:
                flash("Invalid File format :) only images are allowed", category='error')
        
    return redirect(url_for('views.admin'))

@views.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        data = Chairs.query.get(request.form.get('sno'))
        data.title = request.form.get('title')
        data.description = request.form.get('description')
        file = request.files['cover']

        if file.filename == '':
            db.session.commit()
            flash("Chair Updated Successfully", category='success')
            return redirect(url_for('views.admin'))
        else:
            filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
            _ , b = os.path.splitext(filename)
            if b.lower() in ALLOWED_FORMATS:
                if os.path.exists('website/' + data.cover):
                    os.remove('website/' + data.cover)
                file.save(filename)
                flash("Image Updated Successfully", category='success')
                data.cover = filename[8:]
                db.session.commit()
                flash("Chair Updated Successfully", category='success')

            else:
                flash("Invalid File format only images are allowed", category='error')

    return redirect(url_for('views.admin'))


@views.route('/delete/<sno>/', methods=['GET', 'POST'])
@login_required
def delete(sno):
    data = Chairs.query.get(sno)
    if os.path.exists('website/' + data.cover):
        os.remove('website/' + data.cover)
    db.session.delete(data)
    db.session.commit()
    flash("Chair Deleted Successfully", category='success')
    return redirect(url_for('views.admin'))
