""" Projet CoolToGo Alone """
############################################
""" Module by Zahra
𐤟 Création : 2020-03-06
𐤟 Dernière MàJ : 2020-04-12
"""

import psycopg2, psycopg2.extras, sys
from psycopg2 import Error
import DB_Table_Definitions
import socket
from sqlalchemy import create_engine
################ Connexion ################

conn = None
cur = None

def ConnexionDB(): # /!\ Return connection & cursor as tuple
    global conn
    global cur
    try:
        if socket.gethostname()=="zahra-ThinkPad-T440" :
            # Connection parameters on localhost
            conn = psycopg2.connect(dbname="cooool", user="toooo", password="goooo", host="localhost", port="5432")    
        else :
            # Connection parameters on Heroku
            conn = psycopg2.connect(dbname="d74ievmpccqdh6", user="pecrslpcwmptbf", password="3f48aaeb90fa4b6b1aa0d93cd78e67635047214b80b323c584fabcc29b66a160", host="ec2-46-137-177-160.eu-west-1.compute.amazonaws.com", port="5432")
    except:
        print("connection impossible !")
        sys.exit()
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    print("Connection :",conn,"Curseur :", cur)
    return conn, cur

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
    try:
        if socket.gethostname()=="zahra-ThinkPad-T440" :
            # Create engine for postgreSQL
            engine = create_engine('postgresql+psycopg2://toooo:goooo@localhost:5432/cooool',echo=False)    
        else :
            # Create engine for Heroku
            engine = create_engine('postgresql+psycopg2://pecrslpcwmptbf:3f48aaeb90fa4b6b1aa0d93cd78e67635047214b80b323c584fabcc29b66a160@ec2-46-137-177-160.eu-west-1.compute.amazonaws.com:5432/d74ievmpccqdh6',echo=False) 
    except:
        print("Connection impossible !")
        sys.exit()
    return engine

################ Fin ################