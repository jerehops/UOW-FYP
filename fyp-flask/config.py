from os import environ, path
import os
base_dir = path.abspath(path.dirname(__file__))

class Config:
  TESTING = True
  DEBUG = True
  SECRET_KEY = os.urandom(24).hex()
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(base_dir, 'user.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  FLASK_ADMIN_SWATCH = 'cerulean'
  TEMPLATES_AUTO_RELOAD = True
  WTF_CSRF_ENABLED = False
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024
  UPLOAD_FOLDER = path.join('/opt/data/uploads/')
  DEFAULT_FOLDER = path.join('/opt/data/default/')
  ALLOWED_EXTENSIONS = set(['csv'])
  SESSION_COOKIE_NAME = "flask-fyp"