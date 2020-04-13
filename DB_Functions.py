""" Projet CoolToGo Alone """
############################################
""" Module by Zahra
𐤟 Création : 2020-03-06
𐤟 Dernière MàJ : 2020-04-12
"""

import psycopg2
from psycopg2 import Error
from werkzeug.security import generate_password_hash, check_password_hash
import DB_Protocole, DB_Table_Definitions



def recuperation_id(sql_select:str,valeur_inserer:tuple):
    DB_Protocole.cur.execute(sql_select,valeur_inserer)
    try:
        id_table=DB_Protocole.cur.fetchone()[0]
    except:
        id_table=None
    return id_table


def insert_selection(selection_name:str,description:str,lieu_event:str):
    dico= {
        'selection': selection_name,
        'description': description,
        'selection_type': lieu_event}
    try:
        DB_Protocole.Insert_SQL(DB_Table_Definitions.insert_selection,dico)
        return "Ok"
    except (psycopg2.Error, AttributeError) as Error :
        return Error


def insert_cooltogo_validated(id_apidae:str,Lieu_event:str,X:float,Y:float,
                            name:str,Adresse1:str,Adresse2:str,Code_postal:int,
                            Ville:str,Description_Teaser:str,Description:str,Images:str,Publics:str,
                            styleUrl:str,styleHash:str,Type:str,Categories:str,
                            Accessibilite:str,payant:bool,Plus_d_infos_et_horaires:str,
                            Dates_debut:str,Dates_fin:str):

    sql_cooltogo_validated="select id as id_valide from cooltogo_validated where id_apidae = %s "
    id_cooltogo_validated = recuperation_id(sql_cooltogo_validated,(id_apidae,))

    if type(id_cooltogo_validated)!=type(int()):

        dico:dict[str,bool]= {
            'id_apidae': id_apidae,
            'Lieu_event': Lieu_event,
            'X': X,
            'Y' :Y,
            'name': name,
            'Adresse1': Adresse1,
            'Adresse2': Adresse2,
            'Code_postal': Code_postal,
            'Ville': Ville,
            'Description_Teaser': Description_Teaser,
            'Description' : Description,
            'Images': Images,
            'Publics': Publics,
            'styleUrl': styleUrl,
            'styleHash': styleHash,
            'Type': Type,
            'Catégories': Categories,
            'Accessibilité': Accessibilite,
            'payant': payant,
            'Plus_d_infos_et_horaires': Plus_d_infos_et_horaires,
            'Dates_début': Dates_debut,
            'Dates_fin': Dates_fin
            }
        
        try:
            DB_Protocole.Insert_SQL(DB_Table_Definitions.insert_cooltogo_validated,dico)
            id_row=DB_Protocole.cur.fetchone()[0]
        except (psycopg2.Error, AttributeError) as Error :
            print(Error)
    else:
        print('Il y à déja un id_apidae validée')

###############################################################################

def insert_administrator(username:str , password:str,mail:str = None):
    sql_admin="select PKId_Admin from administrators where Admin_Name = %s "
    id_admin = recuperation_id(sql_admin,(username,))
    hash = 'pbkdf2:sha256'
    password_hash = generate_password_hash(password, hash)

    if type(id_admin)!=type(int()):

        dico:dict[str,bool]= {
            'Admin_Name': username,
            'Admin_pwd_hash': password_hash,
            'Admin_email': mail
        }
        try:
            DB_Protocole.Insert_SQL(DB_Table_Definitions.insert_administrators,dico)
            id_admin=DB_Protocole.cur.fetchone()[0]
        except Error :
            print('insert utilisateur echoué' + Error)
    else:
        print('Il y à déja un utilisateur')
    return id_admin

###############################################################################

def connexion_admin(nom_admin:str, password:str, inscription:bool=False):
    '''
    permet de verifier si un utilisateur existe ou pas
    '''
    sql_admin = "select Admin_Name from administrators"
    DB_Protocole.cur.execute(sql_admin)
    list_admin:list = DB_Protocole.cur.fetchall()

    if inscription == False:
        sql_admin = "select Admin_pwd_hash from administrators where Admin_Name = %s "
        DB_Protocole.cur.execute(sql_admin,[nom_admin,])
        
        try :
            mdp_base:str = DB_Protocole.cur.fetchone()[0]
            existe:bool =check_password_hash(mdp_base,password)
        except :
            existe:bool = False
        return existe, list_admin
    else:
        return list_admin

###############################################################################

def create_dict_for_lieu_validated(thelist:list):
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
    Description_Teaser = thelist[10]
    Description = thelist[11]
    Images = thelist[12]
    Publics = thelist[13]
    styleUrl = thelist[14]
    styleHash = thelist[15]
    Type = thelist[16]
    Categories = thelist[17]
    Accessibilite = thelist[18]
    payant = thelist[19]
    Plus_d_infos_et_horaires = thelist[20]
    Dates_debut = thelist[21]
    Dates_fin = thelist[22]

    dict_for_properties = {}
    dict_for_properties.update({"lieu_event": Lieu_event})
    dict_for_properties.update({"x": X})
    dict_for_properties.update({"y": Y})
    dict_for_properties.update({"name": name})
    dict_for_properties.update({"adresse_1": Adresse1})
    dict_for_properties.update({"adresse_2": Adresse2})
    dict_for_properties.update({"code_postal": Code_postal})
    dict_for_properties.update({"ville": Ville})
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
    dict_for_geometry.update({"coordinates": [X,Y]})

    dict_for_lieu_validated ={}
    dict_for_lieu_validated.update({"properties": dict_for_properties})
    dict_for_lieu_validated.update({"geometry": dict_for_geometry})
    dict_for_lieu_validated.update({"type": "Feature"})
    return dict_for_lieu_validated
