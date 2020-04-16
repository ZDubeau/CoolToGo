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
                                'adresse1','adresse2','code_postal','ville','telephone','email','site_web','description_teaser',
                                'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    
    url = 'http://api.apidae-tourisme.com/api/v002/objet-touristique/get-by-id/' + select_id + '?'
    url += "responseFields=id,nom,informations,presentation.descriptifCourt,@all"
    url += '&apiKey='+api_KEY
    url += '&projetId='+project_ID

    re = requests.get(url)
    req = re.json()
    
    dict_for_id = {}

    dict_for_id['id_apidae'] = None
    if 'identifier' in req:
        dict_for_id['id_apidae'] = req['identifier']
#-----------------------------------------------------------------------------------------------------------------------
    sql_select_data = "SELECT id, selection_type FROM selection WHERE selection='"+selectionId+"'"
    DB_Protocole.cur.execute(sql_select_data)
    data = DB_Protocole.cur.fetchall()
    dict_for_id['id_selection'] = data[0][0]
    dict_for_id['lieu_event'] = data[0][1]
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['names'] = None
    if 'gestion' in req:
        if 'membreProprietaire' in req['gestion']:
            if 'nom' in req['gestion']['membreProprietaire']:
                dict_for_id['names'] = req['gestion']['membreProprietaire']['nom']
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['types'] = None
    if 'type' in req:
        dict_for_id['types'] = req['type']
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['longitude'] = None
    dict_for_id['latitude'] = None
    dict_for_id['adresse2'] = None
    dict_for_id['adresse1'] = None
    if 'localisation' in req:
        if 'geolocalisation' in req['localisation']:
            if 'geoJson' in req['localisation']['geolocalisation']:
                if 'coordinates' in req['localisation']['geolocalisation']['geoJson']:
                    dict_for_id['longitude'] = req['localisation']['geolocalisation']['geoJson']['coordinates'][0]
                    dict_for_id['latitude'] = req['localisation']['geolocalisation']['geoJson']['coordinates'][1]
#------------------------------------------------------------------------------------------------------------------------
        if 'adresse' in req['localisation']:
            if 'adresse1' in req['localisation']['adresse']:
                dict_for_id['adresse1'] = req['localisation']['adresse']['adresse1']
            if 'adresse2' in req['localisation']['adresse']:
                dict_for_id['adresse2'] = req['localisation']['adresse']['adresse2']
#------------------------------------------------------------------------------------------------------------------------
    dict_for_id['ville'] = None
    dict_for_id['code_postal'] = None
    if 'localisation' in req:
        if 'adresse' in req['localisation']:
            if 'commune' in req['localisation']['adresse']:
                if 'codePostal' in req['localisation']['adresse']:
                    dict_for_id['code_postal'] = req['localisation']['adresse']['codePostal']
                    if 'nom' in req['localisation']['adresse']['commune']:
                        dict_for_id['ville'] = req['localisation']['adresse']['commune']['nom']
#------------------------------------------------------------------------------------------------------------------------
    dict_for_id['telephone'] = None
    dict_for_id['email'] = None
    dict_for_id['site_web'] = None
    if 'informations' in req:
        if 'moyensCommunication' in req['informations']:
            moyenCommunications = req['informations']['moyensCommunication']
            for values in moyenCommunications :
                if 'type' in values and  'coordonnees' in values :
                    if 'libelleFr' in values['type'] and 'fr' in values['coordonnees'] :
                        if values['type']['libelleFr'] == "Site web (URL)" :
                            dict_for_id['site_web'] = values['coordonnees']['fr']
                        elif values['type']['libelleFr'] == "Téléphone" :
                            dict_for_id['telephone'] = values['coordonnees']['fr']
                        elif values['type']['libelleFr'] == "Mél" :
                            dict_for_id['email'] = values['coordonnees']['fr']    
#------------------------------------------------------------------------------------------------------------------------
    dict_for_id['description_teaser'] = None
    if 'presentation' in req:
        if 'descriptifCourt' in req['presentation']:
            if 'libelleFr' in req['presentation']['descriptifCourt']:
                dict_for_id['description_teaser'] = req['presentation']['descriptifCourt']['libelleFr']
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['images'] = None
    if 'illustrations' in req:
        if 'traductionFichiers' in req['illustrations'][0]:
            if 'url' in req['illustrations'][0]['traductionFichiers'][0]:
                dict_for_id['images'] = req['illustrations'][0]['traductionFichiers'][0]['url']
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['publics'] = None
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['categories'] = None
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['accessibilité'] = None
    if 'prestations' in req:
        if 'tourismesAdaptes' in req['prestations']:
            if 'libelleFr' in req['prestations']['tourismesAdaptes'][0]:
                dict_for_id['accessibilité'] = req['prestations']['tourismesAdaptes'][0]['libelleFr']  
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['payant'] = None
    if 'descriptionTarif' in req:
        if 'gratuit' in req['descriptionTarif']:
            dict_for_id['payant'] = req['descriptionTarif']['gratuit']
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['plus_d_infos_et_horaires'] = None
    if 'gestion' in req:
        if 'membreProprietaire' in req['gestion']:
            if 'siteWeb' in req['gestion']['membreProprietaire']:
                dict_for_id['plus_d_infos_et_horaires'] = req['gestion']['membreProprietaire']['siteWeb']
#-----------------------------------------------------------------------------------------------------------------------
    dict_for_id['date_début'] = None
    dict_for_id['date_fin'] = None
    if 'ouverture' in req:
        if 'periodesOuvertures' in req['ouverture']:
            if 'dateDebut' in req['ouverture']['periodesOuvertures'][0]:
                dict_for_id['date_début'] = req['ouverture']['periodesOuvertures'][0]['dateDebut']
            if 'dateFin' in req['ouverture']['periodesOuvertures'][0]:
                dict_for_id['date_fin'] = req['ouverture']['periodesOuvertures'][0]['dateFin']
  
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
                                'adresse1','adresse2','code_postal','ville','telephone','email','site_web','description_teaser'
                                ,'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    
    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    url += '"selectionIds":["'+selectionId+'"]}'
    count = 100
    try :
        req = requests.get(url).json()
        if "numFound" in req :
            nb_object = int(req["numFound"])
        else :
            print("Oh merde")
            return result_df
        i = 0
        while count*i<nb_object :
            result_df = result_df.append(retrive_data_by_selectionId_by_cent(project_ID,api_KEY,selectionId,count*i,count))
            i+=1
    except :
        print ("problème d'extraction")
    return result_df

def retrive_data_by_selectionId_by_cent(project_ID,api_KEY,selectionId,first,count):
    import pandas as pd
    result_df = pd.DataFrame(columns = ['id_apidae','id_selection','lieu_event','names','types','longitude','latitude',
                                'adresse1','adresse2','code_postal','ville','telephone','email','site_web','description_teaser'
                                ,'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    
    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    url += '"selectionIds":["'+selectionId+'"],'
    url += '"count":"'+count_+'",'
    url += '"first":"'+str(first)+'"}'
    print(url)
    try :
        req = requests.get(url)
        df = pd.json_normalize(req.json(),'objetsTouristiques', errors='ignore')
        for index, row in df.iterrows():
            result_df = result_df.append(retrieve_data_by_id(project_ID,api_KEY,str(row['id']),selectionId))
    except :
        print ("problème d'extraction")
    return result_df
#-----------------------------------------------------------------------------------------------------------------------
def retrive_data_by_multiple_selectionId(project_ID,api_KEY,list_selectionId):
    import pandas as pd
    result_df = pd.DataFrame(columns = ['id_apidae','id_selection','lieu_event','names','types','longitude','latitude',
                                'adresse1','adresse2','code_postal','ville','telephone','email','site_web','description_teaser',
                                'images','publics','categories','accessibilité',
                                'payant','plus_d_infos_et_horaires','date_début','date_fin']) 
    for value in list_selectionId :
        result_df = result_df.append(retrive_data_by_selectionId(project_ID,api_KEY,value))
    result_df.reset_index(inplace=True)
    del result_df['index']    
    return result_df
#-----------------------------------------------------------------------------------------------------------------------