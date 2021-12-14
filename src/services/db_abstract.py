from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class DBAbstract:
    def __init__(self, app: Flask):
        self.connection_string = app.config['SQLALCHEMY_DATABASE_URI']
        self.engine = create_engine(self.connection_string)
        self.Base = declarative_base()
        self.metadata = self.Base.metadata
        self.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine, autoflush=True)
        self.session = self.Session()

    def drop_all(self):
        pass

    def sql_create_db(self):
        pass