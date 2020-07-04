""" 
Projet CoolToGo
----------------------------
Creation date  : 2020-03-06
Last update    : 2020-07-01
----------------------------
"""
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
import DB_Protocole
import DB_Table_Definitions
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
    connexion.close()
    return id_table
# _______________________________________________________________________


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
        connexion.close()
        return "That's ok !"
    except (psycopg2.Error, AttributeError) as Error:
        return Error
# _______________________________________________________________________


# def edit_selection(id_selection: str):
#     dico = {'id': int(id_selection)}
#     print(dico)
#     try:

#         DB_connexion.Insert_SQL(dico)
#         return "Ok"
#     except (psycopg2.Error, AttributeError) as Error:
#         return Error
# _______________________________________________________________________


def insert_project(project_ID: str, api_key: str):
    dico = {
        'project_ID': project_ID,
        'api_key': api_key
    }
    print(dico)
    try:
        connexion = DB_connexion()
        id_project = connexion.Insert_SQL_fetchone(
            project.insert_project, dico)[0]
        connexion.close()
        return id_project
    except (psycopg2.Error, AttributeError) as Error:
        print(Error)
# _______________________________________________________________________


# def insert_cooltogo_validated(id_apidae: str, X: float, Y: float, niveau_fraicheur: str,
#                               Adresse1: str, Adresse2: str, Code_postal: int,
#                               Ville: str, Telephone: str, Email: str, Site_web: str,
#                               Description_Teaser: str, Description: str, Images: str, Publics: str,
#                               Type: str, Categories: str, Accessibilite: str, payant: bool,
#                               Plus_d_infos_et_horaires: str, Dates_debut: str, Dates_fin: str):

#     sql_cooltogo_validated = "SELECT id AS id_valide FROM cooltogo_validated WHERE id_apidae = %s "
#     id_cooltogo_validated = recuperation_id(
#         sql_cooltogo_validated, (id_apidae,))

#     if type(id_cooltogo_validated) != type(int()):

#         dico: dict[str, bool] = {
#             'id_apidae': id_apidae,
#             'Lieu_event': Lieu_event,
#             'X': X,
#             'Y': Y,
#             'name': name,
#             'Adresse1': Adresse1,
#             'Adresse2': Adresse2,
#             'Code_postal': Code_postal,
#             'Ville': Ville,
#             'telephone': Telephone,
#             'email': Email,
#             'site_web': Site_web,
#             'Description_Teaser': Description_Teaser,
#             'Description': Description,
#             'Images': Images,
#             'Publics': Publics,
#             'Type': Type,
#             'Catégories': Categories,
#             'Accessibilité': Accessibilite,
#             'payant': payant,
#             'Plus_d_infos_et_horaires': Plus_d_infos_et_horaires,
#             'Dates_début': Dates_debut,
#             'Dates_fin': Dates_fin
#         }

#         try:
#             print(DB_Table_Definitions.insert_cooltogo_validated, dico)
#             DB_connexion.Insert_SQL(
#                 DB_Table_Definitions.insert_cooltogo_validated, dico)
#             if (niveau_fraicheur != None):
#                 sql_id = "SELECT id FROM cooltogo_validated WHERE id_apidae='"+id_apidae+"'"
#                 DB_connexion.cur.execute(sql_id)
#                 id_cooltogo_validated = DB_connexion.cur.fetchone()[0]
#                 sql_insert_lien = "INSERT INTO lien_niveau_de_fraicheur_cooltogo_validated (id_cooltogo_validated, id_niveau_de_fraicheur) VALUES (" + str(
#                     id_cooltogo_validated) + ", " + niveau_fraicheur + ")"
#                 DB_connexion.cur.execute(sql_insert_lien)
#                 DB_connexion.Commit()
#         except (psycopg2.Error, AttributeError) as Error:
#             print(Error)
#     else:
#         print('There is already a validated id_apidae')
# _______________________________________________________________________


# def update_cooltogo_validated(id_apidae: str, Lieu_event: str, X: float, Y: float,
#                               name: str, niveau_fraicheur: str, Adresse1: str, Adresse2: str,
#                               Code_postal: int, Ville: str, Telephone: str, Email: str,
#                               Site_web: str, Description_Teaser: str, Description: str,
#                               Images: str, Publics: str, Type: str, Categories: str,
#                               Accessibilite: str, payant: bool, Plus_d_infos_et_horaires: str,
#                               Dates_debut: str, Dates_fin: str):

#     sql_cooltogo_validated = "select id as id_valide from cooltogo_validated where id_apidae = %s "
#     id_cooltogo_validated = recuperation_id(
#         sql_cooltogo_validated, (id_apidae,))

#     if type(id_cooltogo_validated) == type(int()):

#         dico: dict[str, bool] = {
#             'id_apidae': id_apidae,
#             'Lieu_event': Lieu_event,
#             'X': X,
#             'Y': Y,
#             'name': name,
#             'Adresse1': Adresse1,
#             'Adresse2': Adresse2,
#             'Code_postal': Code_postal,
#             'Ville': Ville,
#             'telephone': Telephone,
#             'email': Email,
#             'site_web': Site_web,
#             'Description_Teaser': Description_Teaser,
#             'Description': Description,
#             'Images': Images,
#             'Publics': Publics,
#             'Type': Type,
#             'Catégories': Categories,
#             'Accessibilité': Accessibilite,
#             'payant': payant,
#             'Plus_d_infos_et_horaires': Plus_d_infos_et_horaires,
#             'Dates_début': Dates_debut,
#             'Dates_fin': Dates_fin
#         }

#         try:
#             ErrorMessage = DB_connexion.Update_SQL(
#                 DB_Table_Definitions.update_cooltogo_validated, dico)
#             sql_id = "SELECT id FROM cooltogo_validated WHERE id_apidae='"+id_apidae+"'"
#             DB_connexion.cur.execute(sql_id)
#             id_cooltogo_validated = DB_connexion.cur.fetchone()[0]
#             sql_in_lien_niveau_fraicheur_cooltogo_validated = "SELECT id FROM lien_niveau_de_fraicheur_cooltogo_validated WHERE id_cooltogo_validated=" + \
#                 str(id_cooltogo_validated)
#             DB_connexion.cur.execute(
#                 sql_in_lien_niveau_fraicheur_cooltogo_validated)
#             if (DB_connexion.cur.fetchone() == None):
#                 sql_insert_lien = "INSERT INTO lien_niveau_de_fraicheur_cooltogo_validated (id_cooltogo_validated, id_niveau_de_fraicheur) VALUES (" + str(
#                     id_cooltogo_validated) + ", " + niveau_fraicheur + ")"
#                 DB_connexion.cur.execute(sql_insert_lien)
#             else:
#                 sql_update_lien = "UPDATE lien_niveau_de_fraicheur_cooltogo_validated SET id_niveau_de_fraicheur=" + \
#                     niveau_fraicheur + "WHERE id_cooltogo_validated=" + \
#                     str(id_cooltogo_validated)
#                 DB_connexion.cur.execute(sql_update_lien)
#             DB_connexion.Commit()
#         except (psycopg2.Error, AttributeError) as Error:
#             return Error
#     else:
#         return 'Aucun enregistrement correpondant à mettre à jour'
#     if ErrorMessage == "OK":
#         return "Lieu mis à jour !!"
#     else:
#         return ErrorMessage
# _______________________________________________________________________


def insert_administrator(username: str, password: str, mail: str = None):

    id_admin = recuperation_id(admin.select_id_admin, (username,))
    hash = 'pbkdf2:sha256'
    password_hash = generate_password_hash(password, hash)

    if type(id_admin) != type(int()):

        dico: dict[str, bool] = {
            'admin_name': username,
            'admin_pwd_hash': password_hash,
            'admin_email': mail
        }
        try:
            connexion = DB_connexion()
            id_admin = connexion.Insert_SQL_fetchone(
                admin.insert_admin, dico)[0]
            connexion.close()
        except Error:
            print('Failed user insert !' + Error)
    else:
        print('There is already an user !')

    return id_admin
# _______________________________________________________________________


def connexion_admin(nom_admin: str, password: str, inscription: bool = False):
    '''
    permet de verifier si un utilisateur existe ou pas!
    '''
    connexion = DB_connexion()

    list_admin: list = connexion.Query_SQL_fetchall(admin.select_admin)

    if inscription == False:
        try:
            mdp_base: str = connexion.Query_SQL_fetchone(
                admin.select_password, [nom_admin, ])[0]
            existe: bool = check_password_hash(mdp_base, password)
        except:
            existe: bool = False
        connexion.close()
        return existe, list_admin
    else:
        connexion.close()
        return list_admin
# _______________________________________________________________________


def create_dict_for_lieu_validated(thelist: list):

    id_ = thelist[0]
    id_apidae = thelist[1]
    id_selecton = thelist[2]
    type_apidae = thelist[3]
    titre = thelist[4]
    profil_c2g = thelist[5]
    sous_type = thelist[6]
    adresse1 = thelist[7]
    adresse2 = thelist[8]
    code_postal = thelist[9]
    ville = thelist[10]
    altitude = thelist[11]
    latitude = thelist[12]
    longitude = thelist[13]
    telephone = thelist[14]
    email = thelist[15]
    site_web = thelist[16]
    description_courte = thelist[17]
    description_detaillee = thelist[18]
    image = thelist[19]
    publics = thelist[20]
    # if thelist[16] == None:
    #     Publics = None
    # else:
    #     Publics = thelist[16].split(",")
    # Type = thelist[19]
    # if thelist[20] == None:
    #     Categories = None
    # else:
    #     Categories = thelist[20].split(",")
    tourisme_adapte = thelist[21]
    payant = thelist[22]
    animaux_acceptes = thelist[23]
    environnement = thelist[24]
    equipement = thelist[25]
    services = thelist[26]
    periode = thelist[27]
    activites = thelist[28]
    ouverture = thelist[29]
    typologie = thelist[30]
    bons_plans = thelist[31]
    dispositions_speciales = thelist[32]
    service_enfants = thelist[33]

    data = None
    # sql_select_niveau_de_fraicheur = "SELECT nf.niveau_de_fraicheur AS fraicheur FROM niveau_de_fraicheur AS nf INNER JOIN lien_niveau_de_fraicheur_cooltogo_validated AS lnfcv ON nf.id=lnfcv.id_niveau_de_fraicheur WHERE id_cooltogo_validated=" + \
    #     str(id_)

    # connexion = DB_connexion()
    # data = connexion.Query_SQL_fetchone(sql_select_niveau_de_fraicheur)
    # connexion.close()

    if data == None:
        niveau_de_fraicheur = None
    else:
        niveau_de_fraicheur = data[0]

    dict_for_properties = {}
    dict_for_properties.update({"id_apidae": id_apidae})
    dict_for_properties.update({"type_apidae": type_apidae})
    dict_for_properties.update({"titre": titre})
    dict_for_properties.update({"profil_c2g": profil_c2g})
    dict_for_properties.update({"sous_type": sous_type})
    dict_for_properties.update({"adresse_1": adresse1})
    dict_for_properties.update({"adresse_2": adresse2})
    dict_for_properties.update({"code_postal": code_postal})
    dict_for_properties.update({"ville": ville})
    dict_for_properties.update({"latitude": latitude})
    dict_for_properties.update({"latitude": latitude})
    dict_for_properties.update({"longitude": longitude})
    dict_for_properties.update({"telephone": telephone})
    dict_for_properties.update({"email": email})
    dict_for_properties.update({"site_web": site_web})
    dict_for_properties.update({"description_courte": description_courte})
    dict_for_properties.update(
        {"description_detaillee": description_detaillee})
    dict_for_properties.update({"image": [image]})
    dict_for_properties.update({"publics": publics})
    dict_for_properties.update({"tourisme_adapte": tourisme_adapte})
    dict_for_properties.update({"payant": payant})
    dict_for_properties.update({"aanimaux_acceptes": animaux_acceptes})
    dict_for_properties.update({"environnement": environnement})
    dict_for_properties.update({"equipement": equipement})
    dict_for_properties.update({"services": services})
    dict_for_properties.update({"periode": periode})
    dict_for_properties.update({"activites": activites})
    dict_for_properties.update({"ouverture": ouverture})
    dict_for_properties.update({"typologie": typologie})
    dict_for_properties.update({"bons_plans": bons_plans})
    dict_for_properties.update(
        {"dispositions_speciales": dispositions_speciales})
    dict_for_properties.update({"service_enfants": service_enfants})
    # dict_for_properties.update({"id": id})

    dict_for_geometry = {}
    dict_for_geometry.update({"type": "Point"})
    dict_for_geometry.update({"coordinates": [latitude, longitude]})

    dict_for_lieu_validated = {}
    dict_for_lieu_validated.update({"properties": dict_for_properties})
    dict_for_lieu_validated.update({"geometry": dict_for_geometry})
    dict_for_lieu_validated.update({"type": "Feature"})
    #jsons = json.dumps(dict_for_lieu_validated).encode('utf8')
    return dict_for_lieu_validated
# _______________________________________________________________________
