import os
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

spark = Blueprint('spark', __name__)