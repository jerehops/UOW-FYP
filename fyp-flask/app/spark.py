import os, sys
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

spark = Blueprint('spark', __name__)

@spark.route('/movies')
@login_required
def defaultmovie():
    test = test123
    return render_template('analyse.html')
