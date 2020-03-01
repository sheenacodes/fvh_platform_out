import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


POSTGRES_URL = "localhost"  # get_env_variable("POSTGRES_URL")
POSTGRES_USER = "sheena"  # get_env_variable("POSTGRES_USER")
POSTGRES_PW = "sheena"  # get_env_variable("POSTGRES_PW")
POSTGRES_DB = "sp_1"  # get_env_variable("POSTGRES_DB")


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    DEBUG = True
    CSRF_ENABLED = True

    JWT_SECRET_KEY = "jwt-secret-string"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB
    )
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True
    REDIS_URL = "redis://redis:6379/0"
    QUEUES = ["default"]

    KAFKA_BROKERLIST = os.environ.get("KAFKA_BROKERLIST") or "host.docker.internal:9092"
    # SWAGGER = {'swagger'}

    SASL_UNAME = get_env_variable("SASL_UNAME")
    SASL_PASSWORD = get_env_variable("SASL_PASSWORD")
    KAFKA_BROKERS = get_env_variable("KAFKA_BROKERS")
    SECURITY_PROTOCOL = get_env_variable("SECURITY_PROTOCOL")
    SASL_MECHANISM = get_env_variable("SASL_MECHANISM")
    CA_CERT = get_env_variable("CA_CERT")



class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "prod-secret-key"


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "staging-secret-key"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    TESTING = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "test-secret-key"
