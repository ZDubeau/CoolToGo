import requests     # For retrieving Data from Apidae web site
import json         # For be can getting format json
import pandas as pd
from pandas.io.json import json_normalize   # For transorming 'format json' to 'DataFrame pandas'
import DB_Protocole


project_ID = '4364'     # Cool To Go project id
api_KEY = 'ALrtqQmv'    # Apidae API key
select_id = "86749"     # Example id

def retrieve_data_by_id(project_ID,api_KEY,select_id,selectionId):
    
    result_df = pd.DataFrame(columns = ['id_apidae','id_selection','lieu_event','names','types','longitude','latitude',
                                'adresse1','adresse2','code_postal','ville','description_teaser',
                                'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    
    url = 'http://api.apidae-tourisme.com/api/v002/objet-touristique/get-by-id/' + select_id + '?'
    url += "responseFields=id,nom,informations,presentation.descriptifCourt,@all"
    url += '&apiKey='+api_KEY
    url += '&projetId='+project_ID

    re = requests.get(url)
    req = re.json()
    
    dict_for_id = {}

    if 'identifier' in req:
        dict_for_id['id_apidae'] = req['identifier']
    #     if 'membreProprietaire' in req['gestion']:
    #         if 'type' in req['gestion']['membreProprietaire']:
    #             if 'id' in req['gestion']['membreProprietaire']['type']:
    #                 dict_for_id['id_apidae'] = req['gestion']['membreProprietaire']['type']['id']
    #             else:
    #                 dict_for_id['id_apidae'] = None
    #         else:
    #             dict_for_id['id_apidae'] = None
    #     else:
    #         dict_for_id['id_apidae'] = None
    else:
        dict_for_id['id_apidae'] = None
#-----------------------------------------------------------------------------------------------------------------------
    DB_Protocole.ConnexionDB()
    sql_select_data = "SELECT id, selection_type FROM selection WHERE selection='"+selectionId+"'"
    DB_Protocole.cur.execute(sql_select_data)
    data = DB_Protocole.cur.fetchall()
    DB_Protocole.DeconnexionDB()
    dict_for_id['id_selection'] = data[0][0]
    dict_for_id['lieu_event'] = data[0][1]
#-----------------------------------------------------------------------------------------------------------------------
    if 'gestion' in req:
        if 'membreProprietaire' in req['gestion']:
            if 'nom' in req['gestion']['membreProprietaire']:
                dict_for_id['names'] = req['gestion']['membreProprietaire']['nom']
            else:
                dict_for_id['names'] = None
        else:
            dict_for_id['names'] = None
    else:
        dict_for_id['names'] = None
#-----------------------------------------------------------------------------------------------------------------------
    if 'type' in req:
        dict_for_id['types'] = req['type']
    else:
        dict_for_id['types'] = None
#-----------------------------------------------------------------------------------------------------------------------
    if 'localisation' in req:
        if 'geolocalisation' in req['localisation']:
            if 'geoJson' in req['localisation']['geolocalisation']:
                if 'coordinates' in req['localisation']['geolocalisation']['geoJson']:
                    dict_for_id['longitude'] = req['localisation']['geolocalisation']['geoJson']['coordinates'][0]
                    dict_for_id['latitude'] = req['localisation']['geolocalisation']['geoJson']['coordinates'][1]
                else:
                    dict_for_id['longitude'] = None
                    dict_for_id['latitude'] = None
            else:
                dict_for_id['longitude'] = None
                dict_for_id['latitude'] = None
        else:
            dict_for_id['longitude'] = None
            dict_for_id['latitude'] = None
#------------------------------------------------------------------------------------------------------------------------
        if 'adresse' in req['localisation']:
            if 'adresse1' in req['localisation']['adresse']:
                dict_for_id['adresse1'] = req['localisation']['adresse']['adresse1']
            else:
                dict_for_id['adresse1'] = None
            if 'adresse2' in req['localisation']['adresse']:
                dict_for_id['adresse2'] = req['localisation']['adresse']['adresse2']
            else:
                dict_for_id['adresse2'] = None
        else:
            dict_for_id['adresse2'] = None
            dict_for_id['adresse1'] = None
    else:
        dict_for_id['longitude'] = None
        dict_for_id['latitude'] = None
        dict_for_id['adresse2'] = None
        dict_for_id['adresse1'] = None
#------------------------------------------------------------------------------------------------------------------------
    if 'localisation' in req:
        if 'adresse' in req['localisation']:
            if 'commune' in req['localisation']['adresse']:
                if 'codePostal' in req['localisation']['adresse']:
                    dict_for_id['code_postal'] = req['localisation']['adresse']['codePostal']

                    if 'nom' in req['localisation']['adresse']['commune']:
                        dict_for_id['ville'] = req['localisation']['adresse']['commune']['nom']
                    else:
                        dict_for_id['ville'] = None
                else:
                    dict_for_id['code_postal'] = None
            else:
                dict_for_id['ville'] = None
                dict_for_id['code_postal'] = None
        else:
            dict_for_id['ville'] = None
            dict_for_id['code_postal'] = None
    else:
        dict_for_id['ville'] = None
        dict_for_id['code_postal'] = None
#------------------------------------------------------------------------------------------------------------------------
    if 'presentation' in req:
        if 'descriptifCourt' in req['presentation']:
            if 'libelleFr' in req['presentation']['descriptifCourt']:
                dict_for_id['description_teaser'] = req['presentation']['descriptifCourt']['libelleFr']
                #dict_for_id['description_'] = req['presentation']['descriptifCourt']['libelleFr']
            else:
                dict_for_id['description_teaser'] = None
                #dict_for_id['description_'] = None
        else:
            dict_for_id['description_teaser'] = None
            #dict_for_id['description_'] = None
    else:
        dict_for_id['description_teaser'] = None
        #dict_for_id['description_'] = None
#-----------------------------------------------------------------------------------------------------------------------
    if 'illustrations' in req:
        if 'traductionFichiers' in req['illustrations'][0]:
            if 'url' in req['illustrations'][0]['traductionFichiers'][0]:
                dict_for_id['images'] = req['illustrations'][0]['traductionFichiers'][0]['url']
            else:
                dict_for_id['images'] = None
        else:
            dict_for_id['images'] = None
    else:
        dict_for_id['images'] = None
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['publics'] = 'no info'
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['categories'] = 'no info'
#-----------------------------------------------------------------------------------------------------------------------
    if 'prestations' in req:
        if 'tourismesAdaptes' in req['prestations']:
            if 'libelleFr' in req['prestations']['tourismesAdaptes'][0]:
                dict_for_id['accessibilité'] = req['prestations']['tourismesAdaptes'][0]['libelleFr']
            else:
                dict_for_id['accessibilité'] = None
        else:
            dict_for_id['accessibilité'] = None
    else:
        dict_for_id['accessibilité'] = None  
#-----------------------------------------------------------------------------------------------------------------------
    if 'descriptionTarif' in req:
        if 'gratuit' in req['descriptionTarif']:
            dict_for_id['payant'] = req['descriptionTarif']['gratuit']
        else:
            dict_for_id['payant'] = None
    else:
        dict_for_id['payant'] = None
#-----------------------------------------------------------------------------------------------------------------------
    if 'gestion' in req:
        if 'membreProprietaire' in req['gestion']:
            if 'siteWeb' in req['gestion']['membreProprietaire']:
                dict_for_id['plus_d_infos_et_horaires'] = req['gestion']['membreProprietaire']['siteWeb']
            else:
                dict_for_id['plus_d_infos_et_horaires'] = None
        else:
            dict_for_id['plus_d_infos_et_horaires'] = None
    else:
        dict_for_id['plus_d_infos_et_horaires'] = None
#-----------------------------------------------------------------------------------------------------------------------
    if 'ouverture' in req:
        if 'periodesOuvertures' in req['ouverture']:
            if 'dateDebut' in req['ouverture']['periodesOuvertures'][0]:
                dict_for_id['date_début'] = req['ouverture']['periodesOuvertures'][0]['dateDebut']
            else:
                dict_for_id['date_début'] = None
            if 'dateFin' in req['ouverture']['periodesOuvertures'][0]:
                dict_for_id['date_fin'] = req['ouverture']['periodesOuvertures'][0]['dateFin']
            else:
                dict_for_id['date_fin'] = None
        else:
            dict_for_id['date_début'] = None
            dict_for_id['date_fin'] = None
    else:
        dict_for_id['date_début'] = None
        dict_for_id['date_fin'] = None
  
    result_df = result_df.append(dict_for_id,ignore_index=True)
    
    return result_df
#-----------------------------------------------------------------------------------------------------------------------
def retrieve_data_by_id_light(project_ID,api_KEY,select_id):
    
    result_df = pd.DataFrame(columns = ['id_apidae','lieu_event','names','types']) 
    
    url = 'http://api.apidae-tourisme.com/api/v002/objet-touristique/get-by-id/' + select_id + '?'
    url += "responseFields=id,nom,informations,presentation.descriptifCourt,@all"
    url += '&apiKey='+api_KEY
    url += '&projetId='+project_ID

    re = requests.get(url)
    req = re.json()
    
    dict_for_id = {}

    dict_for_id['id_apidae'] = req['gestion']['membreProprietaire']['type']['id']
    dict_for_id['lieu_event'] = 'Lieu'
    dict_for_id['names'] = req['gestion']['membreProprietaire']['nom']
    dict_for_id['types'] = req['type']

    result_df = result_df.append(dict_for_id,ignore_index=True)
    
    return result_df
#-----------------------------------------------------------------------------------------------------------------------
count_ = "100"              #"count":20
first = "0"                 # start from 0

def retrive_data_by_selectionId(project_ID,api_KEY,selectionId):
    import pandas as pd
    result_df = pd.DataFrame(columns = ['id_apidae','id_selection','lieu_event','names','types','longitude','latitude',
                                'adresse1','adresse2','code_postal','ville','description_teaser'
                                ,'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    
    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    url += '"selectionIds":["'+selectionId+'"],'
    url += '"count":"'+count_+'",'
    url += '"first":"'+str(first)+'"}'

    req = requests.get(url)
    df = pd.json_normalize(req.json(),'objetsTouristiques', errors='ignore')
    for index, row in df.iterrows():
        result_df = result_df.append(retrieve_data_by_id(project_ID,api_KEY,str(row['id']),selectionId))
    return result_df
#-----------------------------------------------------------------------------------------------------------------------
def retrive_data_by_multiple_selectionId(project_ID,api_KEY,list_selectionId):
    import pandas as pd
    result_df = pd.DataFrame(columns = ['id_apidae','id_selection','lieu_event','names','types','longitude','latitude',
                                'adresse1','adresse2','code_postal','ville','description_teaser',
                                'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    for value in list_selectionId :
        result_df = result_df.append(retrive_data_by_selectionId(project_ID,api_KEY,value))
        #result_df['ID'] = result_df.index
        #result_df.reset_index(level=0, inplace=True)
        result_df.reset_index(inplace=True)
        del result_df['index']
        #result_df = result_df.reset_index(inplace=True)
        #result_df.columns.values[0]='ID'
        #result_df['ID']= result_df.index + 1
        #result_df.drop_duplicates(subset='ID', keep='last')
    return result_df
#-----------------------------------------------------------------------------------------------------------------------