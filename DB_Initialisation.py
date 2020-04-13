""" Projet CoolToGo Alone """
############################################
""" Module by Zahra
𐤟 Création : 2020-04-12
𐤟 Dernière MàJ : 2020-04-12
"""

import DB_Table_Definitions, DB_Protocole

actions_list = (DB_Table_Definitions.drop_administrators,
                DB_Table_Definitions.drop_message,
                DB_Table_Definitions.drop_selection,
                DB_Table_Definitions.drop_selection_extraction,
                DB_Table_Definitions.drop_cooltogo_from_apidae,
                DB_Table_Definitions.drop_cooltogo_validated,
                DB_Table_Definitions.administrators,
                DB_Table_Definitions.message,
                DB_Table_Definitions.selection,
                DB_Table_Definitions.selection_extraction,
                DB_Table_Definitions.cooltogo_from_apidae,
                DB_Table_Definitions.cooltogo_validated)

if __name__== "__main__":
    DB_Protocole.ConnexionDB()
    for value in actions_list:
        DB_Protocole.cur.execute(value)
        DB_Protocole.Commit() 
    DB_Protocole.DeconnexionDB()
