import logging
from LoggerModule.FileLogger import FileLogger as FileLogger

from DB_Connexion import DB_connexion
import DB_Functions as functions
import Table_category as ctg
import Table_profil as pfl
import Table_Apidae as apidae


def query_database_for_list_of_categories():
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(ctg.select_category)
    del connexion
    ctg_list = []
    for line in data:
        ctg_list.append({'label': line[1], 'value': line[0]})
    return ctg_list


def query_database_for_list_of_profiles():
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(pfl.select_user_profil)
    del connexion
    pfl_list = []
    for line in data:
        pfl_list.append({'label': line[1], 'value': line[0]})
    return pfl_list


def query_database_for_list_of_filtered_locations(categories, profiles):
    connexion = DB_connexion()
    FileLogger.log(
        logging.DEBUG, f"{categories} categories and {profiles} profiles")
    list_of_location = connexion.Query_SQL_fetchall(
        apidae.select_apidae_with_categorie_list_and_profil_list, [profiles, categories])
    locations_list = []
    nb_location = 0
    for location in list_of_location:
        data = connexion.Query_SQL_fetchone(
            apidae.select_apidae_1_id, [location[1]])
        dict_for_apidae, dict_for_geometry = functions.create_dict_for_lieu_validated(
            data)
        # liste properties, geometry
        locations_list.append([dict_for_apidae, dict_for_geometry])
        # locations_list.append(dict_for_properties)  # properties only
        nb_location += 1
    del connexion
    return nb_location, locations_list
