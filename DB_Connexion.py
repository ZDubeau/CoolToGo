"""
Projet CoolToGo
----------------------------
Creation date  : 2020-03-06
Last update    : 2020-06-30
----------------------------
"""
# _______________________________________________________________________

from sqlalchemy.engine import url as sqla_url
from sqlalchemy import create_engine
import os
from psycopg2 import Error
import psycopg2
import psycopg2.extras
import sys

import logging
from LoggerModule.FileLogger import FileLogger as FileLogger
# _______________________________________________________________________


class DB_connexion():

    def __init__(self):

        self.__dbname = os.getenv('DB_NAME')
        self.__user = os.getenv('USER')
        self.__password = os.getenv('PASSWORD')
        self.__host = os.getenv('HOST')
        self.__port = os.getenv('PORTE')
        self.__db_connect_url = sqla_url.URL(
            drivername='postgresql+psycopg2',
            username=self.__user,
            password=self.__password,
            host=self.__host,
            port=self.__port,
            database=self.__dbname)
        try:
            self.__conn = psycopg2.connect(dbname=self.__dbname, user=self.__user,
                                           password=self.__password, host=self.__host, port=self.__port)
            self.__cur = self.__conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            self.__engine = create_engine(self.__db_connect_url, echo=False)
            nb_connexion = self.Query_SQL_fetchone(
                f"SELECT sum(numbackends) FROM pg_stat_database WHERE datname='{self.__dbname}'")[0]
            FileLogger.log(
                logging.DEBUG, f"New connection, cursor and engine created, number of connexion : {nb_connexion}")
        except Error as e:
            if e == 'TooManyConnections':
                sleep(1)
                self.__init__()
            elif e == f'too many connections for role "{self.__user}"':
                sleep(1)
                self.__init__()
            else:
                FileLogger.log(
                    logging.DEBUG, f'Connection impossible !!! error {e}')
                sys.exit()

    def __del__(self):
        self.__cur.close()
        self.__conn.close()
        self.__engine.dispose()
        FileLogger.log(
            logging.DEBUG, f"Connexion closed !!!!")

    def __commit(self):
        self.__conn.commit()

    def Execute_SQL(self, codeSQL, liste=[]):
        self.__cur.execute(codeSQL, liste)

    def Query_SQL_fetchall(self, codeSQL, liste=[]):
        self.__cur.execute(codeSQL, liste)
        return self.__cur.fetchall()

    def Query_SQL_fetchone(self, codeSQL, liste=[]):
        self.__cur.execute(codeSQL, liste)
        return self.__cur.fetchone()

    def Query_SQL_rowcount(self, codeSQL, liste=[]):
        self.__cur.execute(codeSQL, liste)
        return self.__cur.rowcount

    def Insert_SQL(self, codeSQL, liste=[]):
        try:
            self.__cur.execute(codeSQL, liste)
            self.__commit()
        except (psycopg2.Error, AttributeError) as Error:
            print('Erreur insert_SQL', Error)

    def Insert_SQL_fetchone(self, codeSQL, liste=[]):
        try:
            self.__cur.execute(codeSQL, liste)
            self.__commit()
            return self.__cur.fetchone()
        except (psycopg2.Error, AttributeError) as Error:
            print('Erreur insert_SQL_fetchone', Error)

    def Update_SQL(self, codeSQL, liste=[]):
        try:
            self.__cur.execute(codeSQL, liste)
            self.__commit()
        except (psycopg2.Error, AttributeError) as Error:
            return Error

    def Delete_SQL(self, codeSQL, liste=[]):
        try:
            self.__cur.execute(codeSQL, liste)
            self.__commit()
        except (psycopg2.Error, AttributeError) as Error:
            print('Erreur Delete_SQL', Error)
            return Error

    def Create_Table(self, codeSQL):
        try:
            self.__cur.execute(codeSQL)
            self.__commit()
            return 'Create table is OK!'
        except (psycopg2.Error, AttributeError) as Error:
            return Error

    def Drop_Table(self, table):
        try:
            sql = f'DROP TABLE IF EXISTS {table}'
            self.__cur.execute(sql)
        except (psycopg2.Error, AttributeError) as Error:
            print(Error)

    def Drop_Table_Casscade(self, table):
        try:
            sql = f'DROP TABLE IF EXISTS {table} CASCADE'
            sel.__cur.execute(sql)
        except (psycopg2.Error, AttributeError) as Error:
            print(Error)

    def Delete(self, table, condition, liste=[]):
        self.__cur.execute(
            f'DELETE FROM {table} WHERE {condition} = %s;', liste)
        self.__commit()

    # SQLAlchemy engine for pandas

    def cursor(self):
        return self.__cur

    def connexion(self):
        return self.__conn

    def engine(self):
        return self.__engine

    def number_connections(self):
        return self.Query_SQL_fetchone(
            f"SELECT sum(numbackends) FROM pg_stat_database WHERE datname='{self.__dbname}'")[0]
