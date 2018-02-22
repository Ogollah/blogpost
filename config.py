import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try-it-again'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'blogpost.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #post per page
    POSTS_PER_PAGE = 3
