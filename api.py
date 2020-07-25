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
        logging.DEBUG, f"{categories} categories and {profiles} profiles extraction start")
    set_of_all_location = set()
    list_of_location = connexion.Query_SQL_fetchall(apidae.select_apidae)
    for location in list_of_location:
        set_of_all_location.add(location[1])
    nb_locations = len(set_of_all_location)
    nb_locations_extracted = len(list_of_location)
    FileLogger.log(
        logging.DEBUG, f"{nb_locations} different locations in set for {nb_locations_extracted} location extracted !!!")
    set_of_location_id = set()
    list_of_location = connexion.Query_SQL_fetchall(
        apidae.select_apidae_with_categorie_list_edited_and_profil_list_edited, [profiles, categories])
    for location in list_of_location:
        set_of_location_id.add(location[1])
        try:
            set_of_all_location.remove(location[0])
        except:
            FileLogger.log(
                logging.ERROR, f"{location[0]} no more in set of all locations !!!")
    nb_locations_for_json = len(set_of_location_id)
    nb_locations = len(set_of_all_location)
    FileLogger.log(
        logging.DEBUG, f"1st step : {nb_locations} locations for json out of {nb_locations} different locations remaining in set for {nb_locations_extracted} location extracted !!!")
    list_of_location = connexion.Query_SQL_fetchall(
        apidae.select_apidae_with_categorie_list_edited_and_profil_list, [profiles, categories])
    for location in list_of_location:
        set_of_location_id.add(location[1])
        try:
            set_of_all_location.remove(location[0])
        except:
            FileLogger.log(
                logging.ERROR, f"{location[0]} no more in set of all locations !!!")
    nb_locations_for_json = len(set_of_location_id)
    nb_locations = len(set_of_all_location)
    FileLogger.log(
        logging.DEBUG, f"2nd step : {nb_locations} locations for json out of {nb_locations} different locations remaining in set for {nb_locations_extracted} location extracted !!!")
    list_of_location = connexion.Query_SQL_fetchall(
        apidae.select_apidae_with_categorie_list_and_profil_list_edited, [profiles, categories])
    for location in list_of_location:
        set_of_location_id.add(location[1])
        try:
            set_of_all_location.remove(location[0])
        except:
            FileLogger.log(
                logging.ERROR, f"{location[0]} no more in set of all locations !!!")
    nb_locations_for_json = len(set_of_location_id)
    nb_locations = len(set_of_all_location)
    FileLogger.log(
        logging.DEBUG, f"1st step : {nb_locations} locations for json out of {nb_locations} different locations remaining in set for {nb_locations_extracted} location extracted !!!")
    list_of_location = connexion.Query_SQL_fetchall(
        apidae.select_apidae_with_categorie_list_and_profil_list, [profiles, categories])
    for location in list_of_location:
        set_of_location_id.add(location[1])
        try:
            set_of_all_location.remove(location[0])
        except:
            FileLogger.log(
                logging.ERROR, f"{location[0]} no more in set of all locations !!!")
    nb_locations_for_json = len(set_of_location_id)
    nb_locations = len(set_of_all_location)
    FileLogger.log(
        logging.DEBUG, f"1st step : {nb_locations} locations for json out of {nb_locations} different locations remaining in set for {nb_locations_extracted} location extracted !!!")
    locations_list = []
    nb_location = 0
    for id_location in set_of_location_id:
        data = connexion.Query_SQL_fetchone(
            apidae.select_apidae_1_id_with_data_edited, [id_location])
        dict_for_apidae, dict_for_geometry = functions.create_dict_for_lieu_validated(
            data)
        # liste properties, geometry
        locations_list.append(dict_for_apidae)
        # locations_list.append(dict_for_properties)  # properties only
        nb_location += 1
    nb_id_in_set = len(set_of_location_id)
    FileLogger.log(
        logging.DEBUG, f"{nb_id_in_set} in set of location and {nb_location} locations extracted !!!")
    del connexion
    return nb_location, locations_list
