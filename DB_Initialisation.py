"""-------------------------
Creation date  : 2020-03-06
Last update    : 2020-08-03
----------------------------

Be careful, if you run this file you will drop all tables & re-create tables (remove all data) """

# import all tables + file connection that execute tables
import Table_admin
import Table_profil
import Table_Apidae
import Table_project
import Table_message
import Table_category
import Table_freshness
import Table_selection
import Table_extraction
import Table_elementReference
import Table_relation_selection_profil
import Table_relation_selection_category
import Table_relation_eltref_prf
import Table_relation_eltref_ctg
import Table_relation_profil_data_from_apidae
import Table_relation_category_data_from_apidae
import Table_relation_category_apidae_edited
import Table_relation_profil_apidae_edited
from DB_Connexion import DB_connexion


# list (set) of all tables + drop
full_actions_list = (
    Table_message.drop_message,
    Table_elementReference.drop_elementRef,
    Table_project.drop_project,
    Table_selection.drop_selection,
    Table_extraction.drop_selection_extraction,
    Table_Apidae.drop_apidae,
    Table_category.drop_category,
    Table_profil.drop_user_profil,
    Table_relation_eltref_prf.drop_relation_eltref_profil,
    Table_relation_eltref_ctg.drop_relation_eltref_category,
    Table_relation_selection_profil.drop_relation_selection_profil,
    Table_relation_selection_category.drop_relation_selection_category,
    Table_relation_category_data_from_apidae.drop_relation_category_apidae,
    Table_relation_profil_data_from_apidae.drop_relation_profil_apidae,
    Table_admin.drop_admin,
    Table_freshness.drop_freshness_level,
    Table_message.message,
    Table_elementReference.elementRef,
    Table_project.project,
    Table_project.default_project_for_manual_entry,
    Table_selection.selection,
    Table_selection.default_selection_for_manual_entry,
    Table_extraction.selection_extraction,
    Table_Apidae.apidae,
    Table_category.category,
    Table_profil.user_profil,
    Table_relation_eltref_prf.relation_eltref_profil,
    Table_relation_eltref_ctg.relation_eltref_category,
    Table_relation_selection_profil.relation_selection_profil,
    Table_relation_selection_category.relation_selection_category,
    Table_relation_category_data_from_apidae.relation_category_apidae,
    Table_relation_profil_data_from_apidae.relation_profil_apidae,
    Table_admin.admin,
    Table_freshness.freshness_level
)

if __name__ == "__main__":
    connexion = DB_connexion()
    for value in full_actions_list:
        connexion.Insert_SQL(value)
    del connexion
