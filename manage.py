# manage.py


from flask.cli import FlaskGroup

from platform_in import app


cli = FlaskGroup(app)


if __name__ == '__main__':
    cli()