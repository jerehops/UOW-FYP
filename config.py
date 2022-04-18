from os import environ, path
base_dir = path.abspath(path.dirname(__file__))

class Config:
  TESTING = True
  DEBUG = True
  FLASK_ENV = "development"
  SECRET_KEY = "NobodyKnowsThisShhh!!"
  SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI') or 'sqlite:///' + path.join(base_dir, 'test.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  FLASK_ADMIN_SWATCH = 'cerulean'
  TEMPLATES_AUTO_RELOAD = True
  WTF_CSRF_ENABLED = False
  MAX_CONTENT_LENGTH = 16 * 1024 * 1024
  UPLOAD_FOLDER = path.join(base_dir + '/app/datafiles/uploads')
  ALLOWED_EXTENSIONS = set(['csv'])