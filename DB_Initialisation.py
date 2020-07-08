""" ----------------------------
Creation date : 2020-04-12
Last update   : 2020-07-08
----------------------------"""

import Table_admin
import Table_profil
import Table_Apidae
import Table_project
import Table_message
import Table_category
import Table_freshness
import Table_selection
import Table_extraction
import Table_ManualEntry
import Table_elementReference
import Table_relation_selection_profil
import Table_relation_selection_category
from DB_Connexion import DB_connexion
# _____________________________________________

full_actions_list = (
    Table_admin.drop_admin,
    Table_Apidae.drop_apidae,
    Table_message.drop_message,
    Table_project.drop_project,
    Table_category.drop_category,
    Table_profil.drop_user_profil,
    Table_selection.drop_selection,
    Table_ManualEntry.drop_manualEntry,
    Table_freshness.drop_freshness_level,
    Table_elementReference.drop_elementRef,
    Table_extraction.drop_selection_extraction,
    Table_relation_selection_profil.drop_relation_selection_profil,
    Table_relation_selection_category.drop_relation_selection_category,
    Table_admin.admin,
    Table_Apidae.apidae,
    Table_message.message,
    Table_project.project,
    Table_category.category,
    Table_profil.user_profil,
    Table_selection.selection,
    Table_ManualEntry.manualEntry,
    Table_freshness.freshness_level,
    Table_elementReference.elementRef,
    Table_extraction.selection_extraction,
    Table_relation_selection_profil.relation_selection_profil,
    Table_relation_selection_category.relation_selection_category
)

if __name__ == "__main__":
    connexion = DB_connexion()
    for value in full_actions_list:
        connexion.Insert_SQL(value)
    connexion.close()
