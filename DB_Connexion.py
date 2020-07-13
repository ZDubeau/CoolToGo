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
# _______________________________________________________________________


class DB_connexion():

    def __init__(self):

        dbname = os.getenv('DB_NAME')
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        host = os.getenv('HOST')
        port = os.getenv('PORTE')
        db_connect_url = sqla_url.URL(
            drivername='postgresql+psycopg2',
            username=user,
            password=password,
            host=host,
            port=port,
            database=dbname)
        try:
            self.__conn = psycopg2.connect(dbname=dbname, user=user,
                                           password=password, host=host, port=port)
            self.__cur = self.__conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            self.__engine = create_engine(db_connect_url, echo=False)
        except Error as e:
            if e == 'TooManyConnections':
                sleep(10)
                self.__init__()
            else:
                print('Connection impossible !!!')
                sys.exit()

    def close(self):
        self.__cur.close()
        self.__conn.close()
        self.__engine.dispose()

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

    def engine(self):
        return self.__engine
