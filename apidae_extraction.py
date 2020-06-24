""" 
Projet CoolToGo
----------------------------
Creation date : 2020-04-02
Last update   : 2020-06-11
Estimate time :  ?
Spend time    :  ?
----------------------------
"""
# _______________________________________________________________________

# For retrieving Data from Apidae web site
import requests

# For be can getting format json
import json

# Treatment module
import pandas as pd

# For transorming 'format json' to 'DataFrame pandas'
from pandas.io.json import json_normalize

# postgreSQL
import psycopg2
import psycopg2.extras
import sys
from psycopg2 import Error

import threading
from threading import Thread
import time
import queue

# My functions
import DB_Protocole
import Table_selection as slc

# Transformation function of data by id
#from apidae_id_tranformation import restauration_transformation
from transformation import transformation

# _______________________________________________________________________


def retrieve_data_by_id(project_ID, api_KEY, select_id, selectionId):
    result_df = pd.DataFrame(columns=['id_apidae', 'id_selection', 'type_apidae', 'titre', 'adresse1', 'adresse2',
                                      'code_postal', 'ville', 'altitude', 'latitude', 'longitude', 'telephone', 'email',
                                      'site_web', 'description_courte', 'description_detaillee', 'image', 'publics',
                                      'tourisme_adapte', 'payant', 'animaux_acceptes', 'environnement', 'equipement',
                                      'services', 'periode', 'activites', 'ouverture', 'typologie'])

    url = 'http://api.apidae-tourisme.com/api/v002/objet-touristique/get-by-id/' + select_id + '?'
    url += "responseFields=id,nom,informations,presentation.descriptifCourt,@all"
    url += '&apiKey='+api_KEY
    url += '&projetId='+project_ID
    re = requests.get(url)
    req = re.json()

    transfo = transformation(req, [5154, 6143])
    transfo.Execute()
    dict_for_id = transfo.dict_id()
    # if 596 in transfo.list_elements_de_references():
    #     print(dict_for_id['id_apidae'], transfo.list_elements_de_references(
    #     ), "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # # print(transfo.special_elements_descriptions())
    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    connection = DB_Protocole.Connexion()
    curseur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    curseur.execute(
        slc.select_selection_with_type, [selectionId])
    data = curseur.fetchone()
    DB_Protocole.Deconnexion(connection, curseur)
    dict_for_id['id_selection'] = data[0]

    result_df = result_df.append(dict_for_id, ignore_index=True)
    return result_df
# _______________________________________________________________________


# def retrieve_data_by_id_light(project_ID, api_KEY, select_id):

#     result_df = pd.DataFrame(
#         columns=['id_apidae', 'Type_Apidae', 'Titre'])

#     url = 'http://api.apidae-tourisme.com/api/v002/objet-touristique/get-by-id/' + select_id + '?'
#     url += "responseFields=id,nom,informations,presentation.descriptifCourt,@all"
#     url += '&apiKey='+api_KEY
#     url += '&projetId='+project_ID

#     re = requests.get(url)
#     req = re.json()

#     dict_for_id = {}
#     dict_for_id['id_apidae'] = req['gestion']['membreProprietaire']['type']['id']
#     dict_for_id['Titre'] = req['gestion']['membreProprietaire']['nom']
#     dict_for_id['types'] = req['type']

#     result_df = result_df.append(dict_for_id, ignore_index=True)
#     return result_df


# _______________________________________________________________________

count_ = "100"              # "count":20
first = "0"                 # start from 0


def retrive_data_by_selectionId(project_ID, api_KEY, selectionId):
    import pandas as pd
    result_df = pd.DataFrame(columns=['id_apidae', 'id_selection', 'type_apidae', 'titre', 'adresse1', 'adresse2',
                                      'code_postal', 'ville', 'altitude', 'latitude', 'longitude', 'telephone', 'email',
                                      'site_web', 'description_courte', 'description_detaillee', 'image', 'publics',
                                      'tourisme_adapte', 'payant', 'animaux_acceptes', 'environnement', 'equipement',
                                      'services', 'periode', 'activites', 'ouverture', 'typologie'])

    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    url += '"selectionIds":["'+selectionId+'"]}'
    count = 100
    try:
        req = requests.get(url).json()
        if "numFound" in req:
            nb_object = int(req["numFound"])
        else:
            print("Oh merde")
            return result_df
        i = 0
        while count*i < nb_object:
            result_df = result_df.append(retrive_data_by_selectionId_by_cent(
                project_ID, api_KEY, selectionId, count*i, count))
            i += 1
    except ValueError:
        print("problème d'extraction")
    return result_df
# _______________________________________________________________________


def retrive_data_by_selectionId_by_cent(project_ID, api_KEY, selectionId, first, count):
    import pandas as pd
    result_df = pd.DataFrame(columns=['id_apidae', 'id_selection', 'type_apidae', 'titre', 'adresse1', 'adresse2',
                                      'code_postal', 'ville', 'altitude', 'latitude', 'longitude', 'telephone', 'email',
                                      'site_web', 'description_courte', 'description_detaillee', 'image', 'publics',
                                      'tourisme_adapte', 'payant', 'animaux_acceptes', 'environnement', 'equipement',
                                      'services', 'periode', 'activites', 'ouverture', 'typologie'])

    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    url += '"selectionIds":["'+selectionId+'"],'
    url += '"count":"'+str(count)+'",'
    url += '"first":"'+str(first)+'"}'
    try:
        req = requests.get(url)
        df = pd.json_normalize(
            req.json(), 'objetsTouristiques', errors='ignore')
        que = queue.Queue()
        threads_list = list()
        for index, row in df.iterrows():
            #result_df = result_df.append(retrieve_data_by_id(project_ID,api_KEY,str(row['id']),selectionId))
            t = Thread(target=lambda q, arg1, arg2, arg3, arg4: q.put(retrieve_data_by_id(
                arg1, arg2, arg3, arg4)), args=(que, project_ID, api_KEY, str(row['id']), selectionId), daemon=True)
            t.start()
            threads_list.append(t)
        for t in threads_list:
            t.join()
        while not que.empty():
            df = que.get()
            result_df = result_df.append(df)
    except:
        print("problème d'extraction by cent")
    return result_df
# _______________________________________________________________________


def retrive_data_by_multiple_selectionId(project_ID, api_KEY, list_selectionId):
    import pandas as pd
    result_df = pd.DataFrame(columns=['id_apidae', 'id_selection', 'type_apidae', 'titre', 'adresse1', 'adresse2',
                                      'code_postal', 'ville', 'altitude', 'latitude', 'longitude', 'telephone', 'email',
                                      'site_web', 'description_courte', 'description_detaillee', 'image', 'publics',
                                      'tourisme_adapte', 'payant', 'animaux_acceptes', 'environnement', 'equipement',
                                      'services', 'periode', 'activites', 'ouverture', 'typologie'])
    for value in list_selectionId:
        result_df = result_df.append(
            retrive_data_by_selectionId(project_ID, api_KEY, value))
    result_df.reset_index(inplace=True)
    del result_df['index']
    return result_df
# _______________________________________________________________________


def retrieve_selection_list(id_projet, project_ID, api_KEY):
    import pandas as pd
    result_df = pd.DataFrame(
        columns=['id_project', 'selection', 'description'])

    url = 'http://api.apidae-tourisme.com/api/v002/referentiel/selections/?query={'
    url += '"apiKey": "'+api_KEY+'",'
    url += '"projetId":'+project_ID
    url += '}'
    req = requests.get(url).json()
    for line in req:
        dict_for_id = {}
        dict_for_id['id_project'] = id_projet
        dict_for_id['selection'] = line['id']
        dict_for_id['description'] = line['nom']
        result_df = result_df.append(dict_for_id, ignore_index=True)

    return result_df
# _______________________________________________________________________
