from DB_Connexion import DB_connexion
import DB_Functions as functions
import Table_category as ctg
import Table_profil as pfl
import Table_Apidae as apidae


def query_database_for_list_of_categories():
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(ctg.select_category)
    connexion.close()
    ctg_list = []
    for line in data:
        ctg_list.append({'name': line[1], 'id': line[0]})
    return ctg_list


def query_database_for_list_of_profiles():
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(pfl.select_user_profil)
    connexion.close()
    pfl_list = []
    for line in data:
        pfl_list.append({'name': line[1], 'id': line[0]})
    return pfl_list


def query_database_for_list_of_filtered_locations(categories, profiles):
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(apidae.select_apidae)
    connexion.close()
    locations_list = []
    for line in data:
        locations_list.append(functions.create_dict_for_lieu_validated(line))
    return locations_list
