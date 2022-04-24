import os
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.before_app_first_request
def before_app():
    db.create_all()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def profile():
    return render_template('dashboard.html', name=current_user.name)

@main.route('/analyse')
@login_required
def analyse():
    return render_template('analyse.html')

@main.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        path = current_app.config['UPLOAD_FOLDER'] + current_user.name + '/'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file parts')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Please select a file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path + filename)
            flash('File successfully uploaded')
            return redirect('/upload')
        else:
            flash('Allowed file types is csv')
            return redirect(request.url)
