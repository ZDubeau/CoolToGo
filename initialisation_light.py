""" 
Projet CoolToGo
----------------------------
Creation date  : 2020-03-06
Last update    : 2020-07-13
----------------------------
"""
# _______________________________________________________________________

import Table_relation_profil_data_from_apidae
import Table_relation_category_data_from_apidae
from DB_Connexion import DB_connexion
# _______________________________________________________________________


Tables_light = (
    Table_relation_category_data_from_apidae.drop_relation_category_apidae,
    Table_relation_profil_data_from_apidae.drop_relation_profil_apidae,
    Table_relation_category_data_from_apidae.relation_category_apidae,
    Table_relation_profil_data_from_apidae.relation_profil_apidae
)

if __name__ == "__main__":
    connexion = DB_connexion()
    for value in Tables_light:
        connexion.Insert_SQL(value)
    connexion.close()
