# -*- coding: utf-8 -*-
from psycopg2 import extras
import psycopg2


def db_cursor(connection, settings):
    cur = connection.cursor()
    db_conf = settings.DATABASE

    if 'SCHEMA' in db_conf:
        cur.execute('SET search_path TO ' + db_conf['SCHEMA'], ())
    return cur


def db_connect(settings):
    # configura conexión de la base de datos
    _conn_string = (
        ('host=%(HOST)s dbname=%(NAME)s user=%(USER)s ' +
         'password=%(PASSWORD)s') %
        settings.DATABASE
    )

    # conecta a la base de datos
    return psycopg2.connect(
        dsn=_conn_string,
        connection_factory=psycopg2.extras.NamedTupleConnection
    )