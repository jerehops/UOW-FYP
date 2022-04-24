import os, sys
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark_dist_explore import hist
import matplotlib.pyplot as plt
from pyspark.sql import functions as F
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

spark = Blueprint('spark', __name__)

@spark.route('/movies')
@login_required
def defaultmovie():
    return render_template('analyse.html')