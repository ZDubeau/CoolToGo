import requests
import json

project_ID = '4364'
api_KEY = 'ALrtqQmv'

list_code_insee = ["38000","38100"] # Example

def retrive_data_by_insee_code(project_ID,api_KEY,list_code_insee):

    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    first = True
    for value in list_code_insee :
        if first :
            url += '"communeCodesInsee":["'+value+'"'
            first = False
        else :
            url += ',"'+value+'"'
    url += ']}'

    #print(url)
    req = requests.get(url)

    return req.json()

#print(retrive_data_by_insee_code(project_ID,api_KEY,list_code_insee))

###################################################################################################

GPS_coordinates =["45.188529","5.724524"]  # Grenoble coordonate
radius = 30000      # 30km

def retrive_data_by_GPS_coordinates(project_ID,api_KEY,GPS_coordinates,radius):

    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"' + project_ID + '",'
    url += '"apiKey":"' + api_KEY + '",'
    url += '"center":{"type":"Point","coordinates":[' + GPS_coordinates[0] + "," + GPS_coordinates[1] + ']},'
    url += '"radius": ' + str(radius) + '}'
    #print(url)
    req = requests.get(url)

    return req.json()

#print(retrive_data_by_GPS_coordinates(project_ID,api_KEY,GPS_coordinates,radius))

########################################################################################

identifier = "sitraGEO105728" # Example

def retrive_data_by_identifier(project_ID,api_KEY,identifier):
    
    url = 'http://api.apidae-tourisme.com/api/v002/objet-touristique/get-by-identifier/' + identifier + '?'
    url += "responseFields=id,nom,informations,presentation.descriptifCourt,@all"
    url += '&apiKey=' + api_KEY
    url += '&projetId=' + project_ID
    #print(url)
    req = requests.get(url)

    return req.json()

#print("******** : ", retrive_data_by_identifier(project_ID,api_KEY,identifier))

#######################################################################################

list_selectionId = ["86749","86750","86751"]     # Example

GPS_coordinates =["45.188529","5.724524"]
radius = 30000      # 30km

def retrive_data_by_selectionId(project_ID,api_KEY,list_selectionId):

    url = 'http://api.apidae-tourisme.com/api/v002/recherche/list-objets-touristiques?query={'
    url += '"projetId":"'+project_ID+'",'
    url += '"apiKey":"'+api_KEY+'",'
    first = True
    for value in list_selectionId :
        if first :
            url += '"selectionIds":["'+value+'"'
            first = False
        else :
            url += ',"'+value+'"'
    url += ']}'

    #print(url)
    req = requests.get(url)

    return req.json()

#print(retrive_data_by_selectionId(project_ID,api_KEY,list_selectionId))

############################################################################################