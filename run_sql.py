import argparse as argparse
from flask import Flask
from os import environ

from psycopg2._psycopg import OperationalError
from sqlalchemy import create_engine

from src.services import services
from src.services.db_postgres import DBPostgres

services.flask = Flask(__name__)

services.flask.config.from_object('src.configuration.default_settings')
if environ.get('SELF_LEARNING_BACKEND_SETTINGS'):
    services.flask.config.from_envvar('SELF_LEARNING_BACKEND_SETTINGS')

parser = argparse.ArgumentParser(description='Process some integers.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('command', nargs='?',
                    help='''setup - Creates database from scratch, destroys first if exists.
help - Prints this message.''')

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == 'setup':
        try:
            engine = create_engine(f"{services.flask.config['SQLALCHEMY_DATABASE_URI']}/" +
                                   f"{services.flask.config['SQLALCHEMY_DATABASE_NAME']}")
            engine.execute('select t.relname from pg_class t')
        except OperationalError:
            engine = create_engine(services.flask.config['SQLALCHEMY_DATABASE_URI'])
            conn = engine.connect()
            conn.execution_options(isolation_level="AUTOCOMMIT").execute(f'CREATE DATABASE "SelfLearning";')
        services.db = DBPostgres(services.flask)
        services.db.create_db()
    elif args.command == 'help':
        parser.print_help()
    else:
        parser.print_help()
