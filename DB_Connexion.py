""" Projet CoolToGo Alone """

""" Module by Zahra
𐤟 Création : 2020-03-06
𐤟 Dernière MàJ : 2020-06-29
"""




from sqlalchemy.engine import url as sqla_url
from sqlalchemy import create_engine
import os
from psycopg2 import Error
import psycopg2
import psycopg2.extras, sys, json
class DB_connexion():

    def __init__(self):
        with open('info_connection.json') as json_file:
            data = json.load(json_file)
            environnement = os.getenv("FLASK_ENV")
            dbname = data[environnement]['dbname']
            user = data[environnement]['user']
            password = data[environnement]['password']
            host = data[environnement]['host']
            port = data[environnement]['port']
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
        except:
            print("Connection impossible !!!")
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
            print(Error)

    def Insert_SQL_fetchone(self, codeSQL, liste=[]):
        try:
            self.__cur.execute(codeSQL, liste)
            self.__commit()
            return self.__cur.fetchone()
        except (psycopg2.Error, AttributeError) as Error:
            print(Error)

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
            print(Error)
            return Error

    def Create_Table(self, codeSQL):
        try:
            self.__cur.execute(codeSQL)
            self.__commit()
            return "Create table is OK!"
        except (psycopg2.Error, AttributeError) as Error:
            return Error

    def Drop_Table(self, table):
        try:
            sql = f"""DROP TABLE IF EXISTS {table}"""
            self.__cur.execute(sql)
        except (psycopg2.Error, AttributeError) as Error:
            print(Error)

    def Drop_Table_Casscade(self, table):
        try:
            sql = f"""DROP TABLE IF EXISTS {table} CASCADE"""
            sel.__cur.execute(sql)
        except (psycopg2.Error, AttributeError) as Error:
            print(Error)

    def Delete(self, table, condition, liste=[]):
        self.__cur.execute(
            f"""DELETE FROM {table} WHERE {condition} = %s;""", liste)
        self.__commit()

    # SQLAlchemy engine for pandas

    def engine(self):
        return self.__engine
