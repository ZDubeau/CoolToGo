""" Projet CoolToGo Alone """
############################################
""" Module by Zahra
𐤟 Création : 2020-03-06
𐤟 Dernière MàJ : 2020-04-12
"""

import psycopg2, psycopg2.extras, sys, json
from psycopg2 import Error
import DB_Table_Definitions
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import url as sqla_url

################ Connexion ################

conn = None
cur = None

def ConnexionDB(): # /!\ Return connection & cursor as tuple
    global conn
    global cur
    with open('info_connection.json') as json_file:
        data = json.load(json_file)
        environnement = os.getenv("FLASK_ENV")
        dbname = data[environnement]['dbname']
        user = data[environnement]['user']
        password = data[environnement]['password']
        host = data[environnement]['host']
        port = data[environnement]['port']
    try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    except:
        print("connection impossible !!!")
        sys.exit()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #print("Connection :",conn,"Curseur :", cur)
    return conn, cur

def Connexion(): # /!\ Return connection & cursor as tuple
    with open('info_connection.json') as json_file:
        data = json.load(json_file)
        environnement = os.getenv("FLASK_ENV")
        dbname = data[environnement]['dbname']
        user = data[environnement]['user']
        password = data[environnement]['password']
        host = data[environnement]['host']
        port = data[environnement]['port']
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    except:
        print("connection impossible !!")
        sys.exit()
    return connection

def Deconnexion(connection,curseur):
    curseur.close
    connection.close()

def DeconnexionDB():
    cur.close() 
    conn.close()

################ Générale ################

def Commit():
    conn.commit()

def Execute_SQL(CodeSQL, MonTuple):
    cur.execute(CodeSQL, MonTuple)


def Query_SQL(CodeSQL, MonTuple):
    cur.execute(CodeSQL, MonTuple)
    return cur.fetchall()

def Insert_SQL(CodeSQL, dico):
    try:
        cur.execute(CodeSQL, dico)
        Commit()
        return "OK"
    except (psycopg2.Error, AttributeError) as Error :
        return Error

def Update_SQL(CodeSQL, dico):
    try:
        cur.execute(CodeSQL, dico)
        Commit()
        return "OK"
    except (psycopg2.Error, AttributeError) as Error :
        return Error

################ Tables ################

def Create_Table(CodeSQL):
    try:
        cur.execute(CodeSQL)
        Commit()
        return "OK"
    except (psycopg2.Error, AttributeError) as Error :
        return Error

def Drop_Table(table):
    try:
        sql = f"""DROP TABLE IF EXISTS {table}"""
        cur.execute(sql)
    except (psycopg2.Error, AttributeError) as Error :
        print(Error)

def Drop_Table_Casscade(table):
    try:
        sql = f"""DROP TABLE IF EXISTS {table} CASCADE"""
        cur.execute(sql)
    except (psycopg2.Error, AttributeError) as Error :
        print(Error)

def Delete(table, condition, MonTuple):
    cur.execute(f"""DELETE FROM {table} WHERE {condition} = %s;""", MonTuple)
    Commit()

########### SQLAlchemy engine for pandas #############

def make_engine() :
    with open('info_connection.json') as json_file:
        data = json.load(json_file)
    environnement = os.getenv("FLASK_ENV")    
    db_connect_url = sqla_url.URL(
        drivername='postgresql+psycopg2',
        username=data[environnement]['user'],
        password=data[environnement]['password'],
        host=data[environnement]['host'],
        port=data[environnement]['port'],
        database=data[environnement]['dbname'])
    try:
        # Create engine for postgreSQL
        engine = create_engine(db_connect_url,echo=False)    
    except:
        print("Connection impossible !")
        sys.exit()
    return engine

################ Fin ################