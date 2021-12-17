from os import path, walk
from importlib import import_module
from sys import modules

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class DBPostgres:
    def __init__(self, app: Flask):
        self.connection_string = f"{app.config['SQLALCHEMY_DATABASE_URI']}/{app.config['SQLALCHEMY_DATABASE_NAME']}"
        self.engine = create_engine(self.connection_string)
        self.Base = declarative_base()
        self.metadata = self.Base.metadata
        self.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine, autoflush=True)
        self.session = self.Session()

    def create_db(self):
        schemas = []
        file_dir = path.realpath(path.join('src', 'models'))
        for (dirpath, dirnames, filenames) in filter(lambda x: not x[0].endswith('__pycache__') and x[0] != file_dir,
                                                     walk(file_dir)):
            schema = path.basename(dirpath)
            if schema not in schemas:
                schemas.append(schema)
            for filename in filenames:
                filename_without_extension = path.splitext(filename)[0]
                fullname = f'src.models.{schema}.{filename_without_extension}'
                if fullname not in modules:
                    import_module(fullname)
        for schema in schemas:
            self.engine.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE;')
            self.engine.execute(f'CREATE SCHEMA IF NOT EXISTS {schema};')
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        self.Base.metadata.drop_all(self.engine)
        self.Base.metadata.create_all(self.engine)
