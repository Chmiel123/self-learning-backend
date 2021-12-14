from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path, walk
from importlib import import_module
from sys import modules

from src.services.db_abstract import DBAbstract


class DBPostgres(DBAbstract):
    def drop_all(self):
        cnn = self.engine.raw_connection()
        cur = cnn.cursor()
        cur.execute("""
            select s.nspname as s, t.relname as t
            from pg_class t join pg_namespace s on s.oid = t.relnamespace
            where t.relkind = 'r'
            and s.nspname !~ '^pg_' and s.nspname != 'information_schema'
            order by 1,2
            """)
        tables = cur.fetchall()  # make sure they are the right ones

        for t in tables:
            cur.execute(f"drop table if exists {t[0]}.{t[1]} cascade")

        cnn.commit()  # goodbye

    def sql_create_db(self):
        schemas = []
        file_dir = path.realpath(path.join('src', 'models'))
        print(file_dir)
        for (dirpath, dirnames, filenames) in filter(lambda x: not x[0].endswith('__pycache__') and x[0] != file_dir,
                                                     walk(file_dir)):
            schema = path.basename(dirpath)
            if schema not in schemas:
                schemas.append(schema)
            for filename in filenames:
                filename_without_extension = path.splitext(filename)[0]
                fullname = f'src.models.{schema}.{filename_without_extension}'
                print(fullname)
                if fullname not in modules:
                    import_module(fullname)
        for schema in schemas:
            self.engine.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE;')
            self.engine.execute(f'CREATE SCHEMA IF NOT EXISTS {schema};')
        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        self.Base.metadata.drop_all(self.engine)
        self.Base.metadata.create_all(self.engine)
