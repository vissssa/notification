"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""
# import click
from flask import Flask

from .extenions import db
from .views import api


def create_app():
    app = Flask('bluelog')
    app.config.from_object('config')

    register_extensions(app)
    register_blueprints(app)
    # register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api)

# def register_commands(app):
#     @app.cli.command()
#     def createdb():
#         """create all tables."""
#         click.echo('Initializing the database...')
#         db.create_all()
#
#     @app.cli.command()
#     @click.option('--migrate', is_flag=True, help='Create after drop.')
#     def initdb(migrate):
#         """Initialize the database."""
#         if migrate:
#             click.confirm('This operation will delete the database, do you want to continue?', abort=True)
#             db.drop_all()
#             click.echo('Drop tables.')
#         db.create_all()
#         click.echo('Initialized database.')
