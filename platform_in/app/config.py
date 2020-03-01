import os
basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

POSTGRES_URL = "localhost" #get_env_variable("POSTGRES_URL")
POSTGRES_USER = "sheena"  #get_env_variable("POSTGRES_USER")
POSTGRES_PW = "sheena"   #get_env_variable("POSTGRES_PW")
POSTGRES_DB = "sp_1" #get_env_variable("POSTGRES_DB")

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    DEBUG = True
    CSRF_ENABLED = True
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SWAGGER = {'swagger'}



class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True