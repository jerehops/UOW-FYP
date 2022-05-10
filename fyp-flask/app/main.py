import os
from sqlalchemy import false, true, desc
from flask import Blueprint, render_template, request, flash, redirect, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pandas as pd
from .models import History
from . import db

main = Blueprint('main', __name__)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

#####################################
## Default Routes and Dashboard
#####################################

@main.before_app_first_request
def before_app():
    db.create_all()

@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html', fName=current_user.firstname, lName=current_user.lastname)
    else:
        return render_template('index.html')
        
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', fName=current_user.firstname, lName=current_user.lastname)

#####################################
## Routes for default data
#####################################

@main.route('/options')
@login_required
def options():
    return render_template('options.html')

@main.route('/movies')
@login_required
def movies():
    return render_template('movies.html')

#####################################
## Routes for Uploading Files
#####################################

@main.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        path = current_app.config['UPLOAD_FOLDER'] + str(current_user.id) + '/'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        if 'files[]' not in request.files:
            res = jsonify({'message' : 'No file part in the request'})
            return res
        files = request.files.getlist('files[]')
        for file in files:
            if not allowed_file(file.filename):
                filecheck = false
                res = jsonify({'message' : 'Only CSV is allowed'})
                return res
            else: 
                filecheck = true
        if (filecheck):
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(path + filename)
                    success = True
        if success:
            res = jsonify({'message' : 'Files successfully uploaded'})
            return res

#####################################
## Routes uploaded data
#####################################

@main.route('/analyse')
@login_required
def analyse():
    fileList = []
    path = current_app.config['UPLOAD_FOLDER'] + str(current_user.id) + '/'
    if (os.path.exists(path)):
        fileList = os.listdir(current_app.config['UPLOAD_FOLDER'] + str(current_user.id) + '/')
    return render_template('analyse.html', fileList=fileList, id=str(current_user.id))

#####################################
## Routes historic data
#####################################

@main.route('/history')
def history():
    data_query = History.query.filter_by(user_id=str(current_user.id)).order_by(History.id.desc()).limit(10).all()
    return render_template('history.html', data=data_query)