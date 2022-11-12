from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Chairs
from . import db
import os

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/chairs/'
ALLOWED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

@views.route('/')
def home():
    return render_template('index.html')

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
        sp = request.form.get('sell')
        dp = request.form.get('discount')
        desc = request.form.get('description')
        
        if file.filename == '':
            flash("No file selected", category='error')
            return redirect(request.url)
        else:
            _ , b = os.path.splitext(secure_filename(file.filename))
            if b.lower() in ALLOWED_FORMATS:
                filename = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(filename)
                print(filename[8:])
                db.session.add(Chairs(title=title, cover=filename[8:], sell_price=sp, disc_price=dp, description=desc))
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
        data.sell_price = request.form.get('sell')
        data.disc_price = request.form.get('discount')
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
