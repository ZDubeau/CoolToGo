""" 
Projet CoolToGo
----------------------------
Creation date : 2020-04-12
Last update   : 2020-06-16
Estimate time : 5 minutes
Spend time    : 5 minutes
----------------------------
"""
# _______________________________________________________________________
import Table_Apidae
import Table_project
import Table_selection
import Table_extraction
import Table_admin
import Table_category
import Table_profil
import Table_freshness
import DB_Protocole
import DB_Table_Definitions
# _______________________________________________________________________
# DB_Table_Definitions.drop_administrators,DB_Table_Definitions.administrators,
# DB_Table_Definitions.drop_lien_niveau_de_fraicheur_cooltogo_validated,
# DB_Table_Definitions.lien_niveau_de_fraicheur_cooltogo_validated,

full_actions_list = (DB_Table_Definitions.drop_message,
                     Table_project.drop_project,
                     Table_selection.drop_selection,
                     Table_extraction.drop_selection_extraction,
                     Table_Apidae.drop_apidae,
                     DB_Table_Definitions.drop_cooltogo_validated,
                     Table_freshness.drop_freshness_level,
                     Table_admin.drop_admin,
                     Table_category.drop_category,
                     Table_profil.drop_user_profil,
                     DB_Table_Definitions.message,
                     Table_project.project,
                     Table_selection.selection,
                     Table_extraction.selection_extraction,
                     Table_Apidae.apidae,
                     DB_Table_Definitions.cooltogo_validated,
                     Table_freshness.freshness_level,
                     Table_admin.admin,
                     Table_category.category,
                     Table_profil.user_profil,)

# ligth_actions_list = (DB_Table_Definitions.drop_message,
#                       Table_project.drop_project,
#                       Table_selection.drop_selection,
#                       Table_extraction.drop_selection_extraction,
#                       Table_Apidae.drop_apidae,
#                       DB_Table_Definitions.drop_cooltogo_validated,
#                       DB_Table_Definitions.drop_lien_niveau_de_fraicheur_cooltogo_validated,
#                       Table_admin.drop_admin,
#                       Table_category.drop_category,
#                       DB_Table_Definitions.message,
#                       Table_project.project,
#                       Table_selection.selection,
#                       Table_extraction.selection_extraction,
#                       Table_Apidae.apidae,
#                       DB_Table_Definitions.cooltogo_validated,
#                       DB_Table_Definitions.lien_niveau_de_fraicheur_cooltogo_validated,
#                       Table_admin.admin,
#                       Table_category.category)

if __name__ == "__main__":
    DB_Protocole.ConnexionDB()
    for value in full_actions_list:
        DB_Protocole.cur.execute(value)
        DB_Protocole.Commit()
    DB_Protocole.DeconnexionDB()
