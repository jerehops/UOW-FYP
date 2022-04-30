from os import environ, path
base_dir = path.abspath(path.dirname(__file__))

class Config:
  TESTING = True
  DEBUG = True
  SECRET_KEY = "NobodyKnowsThisShhh!!"
  SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI') or 'sqlite:///' + path.join(base_dir, 'user.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  FLASK_ADMIN_SWATCH = 'cerulean'
  TEMPLATES_AUTO_RELOAD = True
  WTF_CSRF_ENABLED = False
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024
  DATABASE_URI = path.join(base_dir + '/app/database/user.db')
  UPLOAD_FOLDER = path.join(base_dir + '/data/uploads/')
  DEFAULT_FOLDER = path.join(base_dir + '/app/data/default/')
  ALLOWED_EXTENSIONS = set(['csv'])