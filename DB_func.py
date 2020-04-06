import psycopg2, psycopg2.extras, sys
import pandas as pd
from pandas import DataFrame
import numpy as np
import traceback
#import request_apidae as rp
from sqlalchemy import create_engine
import apidae_extraction as apex  # my function

def connect():
    """ Connect to the PostgreSQL database server """
    global conn
    global cur
    try:
        conn = psycopg2.connect(dbname="cooool",user="toooo",password="goooo",host="localhost",port="5432")
        print('Connecting to the PostgreSQL database...')

    except (Exception,psycopg2.Error) as error:
            print("I am unable to connect to the database")
            print(error)
    
    return conn

drops = (
    """
    DROP TABLE IF EXISTS cooltogo;
    """
    ,
    """
    DROP TABLE IF EXISTS cooltogo_light;
    """,
    """
    CREATE TABLE IF NOT EXISTS cooltogo (
        id SERIAL PRIMARY KEY,
        lieu_event TEXT,
        names TEXT,
        types TEXT,
        latitude FLOAT,
        longitude FLOAT,
        adresse1 VARCHAR(100),
        adresse2 VARCHAR(100),
        code_postal VARCHAR(10),
        ville TEXT,
        description_teaser TEXT,
        description_ TEXT,
        images TEXT,
        publics VARCHAR(20),
        categories VARCHAR(40),
        accessibilité VARCHAR(40),
        payant BOOL,
        plus_d_infos_et_horaires VARCHAR(60),
        date_début DATE,
        date_fin DATE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cooltogo_light (
        id SERIAL PRIMARY KEY,
        lieu_event TEXT,
        names TEXT,
        types TEXT)
        """)

def query(conn,requete):
    """ Curseur """
    cur = conn.cursor()
    cur.execute(requete)

def query_params(conn,requete,params):
    cur = conn.cursor()
    cur.execute(requete,params)

def insert_data():

    df = apex.retrieve_data_by_id(apex.project_ID,apex.api_KEY,apex.select_id)
    # dialect+driver://username:password@host:port/database
    engine = create_engine('postgresql+psycopg2://toooo:goooo@localhost:5432/cooool',echo=False)
    result = df.to_sql('cooltogo',con=engine, index=False, if_exists='append')

    df_light = apex.retrieve_data_by_id_light(apex.project_ID,apex.api_KEY,apex.select_id)
    # dialect+driver://username:password@host:port/database
    result_light = df_light.to_sql('cooltogo_light',con=engine, index=False, if_exists='append')

    #print(df_light)

if __name__== "__main__":
    with connect() as conn:
        for value in drops:
            query(conn,value)
        conn.commit() 
        try:
            insert_data()
        except Exception as e:
            print(traceback.format_exc())
        finally:
            conn.commit()
