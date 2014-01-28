# -*- coding: utf-8 -*-
"""
Connection module

"""
from __future__ import division, print_function, unicode_literals
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras  # load the psycopg extras module


class DB():
    """
    Connection DB

    """
    connection = None
    DB = None

    @staticmethod
    def commit():
        (DB.connection).commit()

    @staticmethod
    def connect(settings):
        """
        Connects to a base

        conn: host=localhost dbname=db_name user=postgres

        """
        _conn_string = (
            ('host=%(HOST)s dbname=%(NAME)s user=%(USER)s ' +
             'password=%(PASSWORD)s') %
            settings.DATABASE[settings.HOSTNAME]
        )

        # DB.conn_string = _conn_string
        DB.connection = psycopg2.connect(
            dsn=_conn_string,
            connection_factory=psycopg2.extras.NamedTupleConnection)

        DB.settings = settings

    @staticmethod
    def cursor():
        cur = DB.connection.cursor()
        dbconf = DB.settings.DATABASE[DB.settings.HOSTNAME]

        if 'SCHEMA' in dbconf:
            DB.execute(cur, 'SET search_path TO ' + dbconf['SCHEMA'])
        return cur

    @staticmethod
    def create_database(database_settings, settings, database_name):
        """

        """
        _conn_string = (
            ('host=%(HOST)s dbname=%(NAME)s user=%(USER)s ' +
             'password=%(PASSWORD)s') % database_settings
        )

        conn = psycopg2.connect(dsn=_conn_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()
        dbconf = settings.DATABASE[settings.HOSTNAME]

        if 'SCHEMA' in dbconf:
            DB.execute(cur, 'SET search_path TO ' + dbconf['SCHEMA'])
        return cur

    @staticmethod
    def execute(cursor, statement, arg=()):
        """

        """
        cursor.execute(statement, arg)
