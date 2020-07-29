"""----------------------------
Creation date  : 2020-03-06
Last update    : 2020-07-16
----------------------------"""
# _______________________________________________________________________

# postgreSQL module
import psycopg2
from psycopg2 import Error

# Comprehensive WSGI web application library
from werkzeug.security import generate_password_hash, check_password_hash
import json
# enumerations
from enum import Enum

# My functions
import Table_admin as admin
import Table_Apidae as api
import Table_project as project
import Table_selection as selection
from DB_Connexion import DB_connexion
# _______________________________________________________________________


def recuperation_id(sql_select: str, valeur_inserer: tuple):
    connexion = DB_connexion()
    try:
        id_table = connexion.Query_SQL_fetchone(sql_select, valeur_inserer)[0]
    except:
        id_table = None
    del connexion
    return id_table


def insert_selection(project_ID: str, api_key: str, selection_name: str, description: str):

    dico = {
        'project_ID': project_ID,
        'api_key': api_key,
        'selection': selection_name,
        'description': description
    }
    try:
        connexion = DB_connexion()
        connexion.Insert_SQL(selection.insert_selection, dico)
        del connexion
        return "That's ok !"
    except (psycopg2.Error, AttributeError) as Error:
        return Error


# def edit_selection(id_selection: str):
#     dico = {'id': int(id_selection)}
#     print(dico)
#     try:
#         DB_connexion.Insert_SQL(dico)
#         return "Ok"
#     except (psycopg2.Error, AttributeError) as Error:
#         return Error


def insert_project(project_ID: str, api_key: str):

    dico = {
        'project_ID': project_ID,
        'api_key': api_key
    }
    try:
        connexion = DB_connexion()
        id_project = connexion.Insert_SQL_fetchone(
            project.insert_project, dico)[0]
        del connexion
        return id_project
    except (psycopg2.Error, AttributeError) as Error:
        print(Error)


def insert_administrator(username: str, password: str, mail: str = None):

    id_admin = recuperation_id(admin.select_id_admin, (username,))
    hash = 'pbkdf2:sha256'
    password_hash = generate_password_hash(password, hash)
    if type(id_admin) != type(int()):
        dico: dict[str, bool] = {
            'admin_name': username,
            'admin_pwd_hash': password_hash,
            'admin_email': mail}
        try:
            connexion = DB_connexion()
            id_admin = connexion.Insert_SQL_fetchone(
                admin.insert_admin, dico)[0]
            del connexion
        except Error:
            print('Failed user insert !' + Error)
    else:
        print('There is already an user !')
    return id_admin


def connexion_admin(nom_admin: str, password: str, inscription: bool = False):
    '''permet de verifier si un utilisateur existe ou pas!'''

    connexion = DB_connexion()

    list_admin: list = connexion.Query_SQL_fetchall(admin.select_admin)

    if inscription == False:
        try:
            mdp_base: str = connexion.Query_SQL_fetchone(
                admin.select_password, [nom_admin, ])[0]
            existe: bool = check_password_hash(mdp_base, password)
        except:
            existe: bool = False
        del connexion
        return existe, list_admin
    else:
        del connexion
        return list_admin


def create_dict_for_lieu_validated(thelist: list):

    # id_ = thelist[0]
    id_apidae = thelist[1]
    # id_selecton = thelist[2]
    type_apidae = thelist[2]
    titre = thelist[3]
    profil_c2g = thelist[4]
    categorie_c2g = thelist[5]
    adresse1 = thelist[6]
    adresse2 = thelist[7]
    code_postal = thelist[8]
    ville = thelist[9]
    altitude = thelist[10]
    longitude = thelist[11]
    latitude = thelist[12]
    telephone = thelist[13]
    email = thelist[14]
    site_web = thelist[15]
    description_courte = thelist[16]
    description_detaillee = thelist[17]
    image = thelist[18]
    publics = thelist[19]
    tourisme_adapte = thelist[20]
    payant = thelist[21]
    # animaux_acceptes = thelist[23]
    environnement = thelist[22]
    # equipement = thelist[25]
    # services = thelist[26]
    # periode = thelist[27]
    # activites = thelist[28]
    ouverture = thelist[23]
    date_debut = thelist[24]
    date_fin = thelist[25]
    # typologie = thelist[30]
    # bons_plans = thelist[31]
    # dispositions_speciales = thelist[32]
    # service_enfants = thelist[33]

    data = None
    # sql_select_niveau_de_fraicheur = "SELECT nf.niveau_de_fraicheur AS fraicheur FROM niveau_de_fraicheur AS nf INNER JOIN lien_niveau_de_fraicheur_cooltogo_validated AS lnfcv ON nf.id=lnfcv.id_niveau_de_fraicheur WHERE id_cooltogo_validated=" + \
    #     str(id_)
    # connexion = DB_connexion()
    # data = connexion.Query_SQL_fetchone(sql_select_niveau_de_fraicheur)
    # del connexion

    if data == None:
        niveau_de_fraicheur = None
    else:
        niveau_de_fraicheur = data[0]

    dict_for_properties = {}
    dict_for_properties.update({"id": id_apidae})
    dict_for_properties.update({"type": type_apidae})
    dict_for_properties.update({"title": titre})
    dict_for_properties.update({"address": adresse1})
    dict_for_properties.update({"adresse2": adresse2})
    dict_for_properties.update({"code_postal": code_postal})
    dict_for_properties.update({"city": ville})
    dict_for_properties.update({"altitude": altitude})
    dict_for_properties.update({"longitude": longitude})
    dict_for_properties.update({"latitude": latitude})
    dict_for_properties.update({"tel": telephone})
    dict_for_properties.update({"mail": email})
    dict_for_properties.update({"url": site_web})
    dict_for_properties.update({"description_short": description_courte})
    dict_for_properties.update({"description": description_detaillee})
    dict_for_properties.update({"images": [image]})
    dict_for_properties.update({"public": publics})
    dict_for_properties.update({"accessibility": tourisme_adapte})
    dict_for_properties.update({"paying": payant})
    dict_for_properties.update({"environment": environnement})
    dict_for_properties.update({"opening": ouverture})
    dict_for_properties.update({"date_start": date_debut})
    dict_for_properties.update({"date_end": date_fin})
    dict_for_properties.update({"profiles": profil_c2g})
    dict_for_properties.update({"categories": categorie_c2g})
    # dict_for_properties.update({"animaux_acceptes": animaux_acceptes})
    # dict_for_properties.update({"equipement": equipement})
    # dict_for_properties.update({"services": services})
    # dict_for_properties.update({"periode": periode})
    # dict_for_properties.update({"activites": activites})
    # dict_for_properties.update({"typologie": typologie})
    # dict_for_properties.update({"bons_plans": bons_plans})
    # dict_for_properties.update({"dispositions_speciales": dispositions_speciales})
    # dict_for_properties.update({"service_enfants": service_enfants})
    # dict_for_properties.update({"id": id})

    dict_for_geometry = {}
    dict_for_geometry.update({"type": "Point"})
    dict_for_geometry.update({"coordinates": [longitude, latitude]})

    dict_for_apidae = dict()
    dict_for_apidae.update({"type": "Feature"})
    dict_for_apidae.update({"properties": dict_for_properties})
    dict_for_apidae.update({"geometry": dict_for_geometry})

    return dict_for_apidae, dict_for_geometry
