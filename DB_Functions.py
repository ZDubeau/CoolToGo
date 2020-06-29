""" 
Projet CoolToGo
----------------------------
Creation date  : 2020-03-06
Last update    : 2020-06-26
Estimate time  : 30 minutes
Spend time     : 15 minutes
----------------------------
"""
# _______________________________________________________________________

# postgreSQL module
import psycopg2
from psycopg2 import Error

# Comprehensive WSGI web application library
from werkzeug.security import generate_password_hash, check_password_hash

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
        connexion.Insert_SQL(project.insert_project, dico)
        connexion.close()
        return "Ok"
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
    Lieu_event = thelist[2]
    X = thelist[3]
    Y = thelist[4]
    name = thelist[5]
    Adresse1 = thelist[6]
    Adresse2 = thelist[7]
    Code_postal = thelist[8]
    Ville = thelist[9]
    telephone = thelist[10]
    email = thelist[11]
    site_web = thelist[12]
    Description_Teaser = thelist[13]
    Description = thelist[14]
    Images = thelist[15]
    if thelist[16] == None:
        Publics = None
    else:
        Publics = thelist[16].split(",")
    Type = thelist[19]
    if thelist[20] == None:
        Categories = None
    else:
        Categories = thelist[20].split(",")
    Accessibilite = thelist[21]
    payant = thelist[22]
    Plus_d_infos_et_horaires = thelist[23]
    Dates_debut = thelist[24]
    Dates_fin = thelist[25]
    DB_connexion.ConnexionDB()
    sql_select_niveau_de_fraicheur = "SELECT nf.niveau_de_fraicheur AS fraicheur FROM niveau_de_fraicheur AS nf INNER JOIN lien_niveau_de_fraicheur_cooltogo_validated AS lnfcv ON nf.id=lnfcv.id_niveau_de_fraicheur WHERE id_cooltogo_validated=" + \
        str(id_)

    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchone(sql_select_niveau_de_fraicheur)
    connexion.close()

    if data == None:
        niveau_de_fraicheur = None
    else:
        niveau_de_fraicheur = data[0]

    dict_for_properties = {}
    dict_for_properties.update({"lieu_event": Lieu_event})
    dict_for_properties.update({"x": X})
    dict_for_properties.update({"y": Y})
    dict_for_properties.update({"name": name})
    dict_for_properties.update({"niveau_de_fraicheur": niveau_de_fraicheur})
    dict_for_properties.update({"adresse_1": Adresse1})
    dict_for_properties.update({"adresse_2": Adresse2})
    dict_for_properties.update({"code_postal": Code_postal})
    dict_for_properties.update({"ville": Ville})
    dict_for_properties.update({"telephone": telephone})
    dict_for_properties.update({"email": email})
    dict_for_properties.update({"site_web": site_web})
    dict_for_properties.update({"description_teaser": Description_Teaser})
    dict_for_properties.update({"images": Images})
    dict_for_properties.update({"publics": Publics})
    dict_for_properties.update({"type": Type})
    dict_for_properties.update({"categories": Categories})
    dict_for_properties.update({"description": Description})
    dict_for_properties.update({"accessibility": Accessibilite})
    dict_for_properties.update({"paid": payant})
    dict_for_properties.update({"info_hours": Plus_d_infos_et_horaires})
    dict_for_properties.update({"start_date": Dates_debut})
    dict_for_properties.update({"end_date": Dates_fin})
    dict_for_properties.update({"id": id_})

    dict_for_geometry = {}
    dict_for_geometry.update({"type": "Point"})
    dict_for_geometry.update({"coordinates": [X, Y]})

    dict_for_lieu_validated = {}
    dict_for_lieu_validated.update({"properties": dict_for_properties})
    dict_for_lieu_validated.update({"geometry": dict_for_geometry})
    dict_for_lieu_validated.update({"type": "Feature"})
    return dict_for_lieu_validated
# _______________________________________________________________________
