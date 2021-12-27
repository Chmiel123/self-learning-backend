import unittest
import sys
import coverage
from flask import Flask
from os import environ, path

from psycopg2._psycopg import OperationalError
from sqlalchemy import create_engine

COV = coverage.coverage(
    branch=True,
    include='/*',
    omit=[
        '/test/*',
        'venv/*',
        '/usr/*',
        'C:/Program Files/*'
    ]
)
COV.start()

from src.services import services
from src.services.db_postgres import DBPostgres

services.flask = Flask(__name__)

services.flask.config.from_object('src.configuration.default_settings')
services.flask.config.from_object('src.configuration.test_settings')
if environ.get('SELF_LEARNING_BACKEND_SETTINGS'):
    services.flask.config.from_envvar('SELF_LEARNING_BACKEND_SETTINGS')

try:
    engine = create_engine(
        f"{services.flask.config['SQLALCHEMY_DATABASE_URI']}/{services.flask.config['SQLALCHEMY_DATABASE_NAME']}")
    engine.execute('select t.relname from pg_class t')
except OperationalError:
    engine = create_engine(services.flask.config['SQLALCHEMY_DATABASE_URI'])
    conn = engine.connect()
    conn.execution_options(isolation_level="AUTOCOMMIT")\
        .execute(f'CREATE DATABASE "{services.flask.config["SQLALCHEMY_DATABASE_NAME"]}";')

from src import app

pattern = ''
if len(sys.argv) > 1:
    pattern = sys.argv[1]
pattern = f'*{pattern}*_test.py'

print(f'pattern: {pattern}\n')

tests = unittest.TestLoader().discover('src/test/', pattern=pattern)
result = unittest.TextTestRunner(verbosity=2).run(tests)

if result.wasSuccessful():
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = path.abspath(path.dirname(__file__))
    covdir = path.join(basedir, 'tmp/coverage')
    COV.html_report(directory=covdir)
    indexPath = path.abspath(covdir + '/index.html')
    print('HTML version: file://%s' % indexPath)
    COV.erase()