""" 
Projet CoolToGo
----------------------------
Creation date : 2020-06-11
Last update : 2020-06-20
----------------------------
"""

drop_relation_profil_apidae = """
                DROP TABLE IF EXISTS relation_profil_data_from_apidae CASCADE;
                """

relation_profil_apidae = """
            CREATE TABLE IF NOT EXISTS relation_profil_data_from_apidae (
                id_relation_profil_apidae SERIAL PRIMARY KEY,
                id_profil BIGINT REFERENCES profil ON DELETE CASCADE,
                id_data_from_apidae BIGINT REFERENCES data_from_apidae ON DELETE CASCADE
            )"""

insert_relation_profil_apidae = """
                    INSERT INTO relation_profil_data_from_apidae (id_profil, id_data_from_apidae)
                    VALUES (%s, %s) 
                    returning id_relation_profil_apidae;
                    """


delete_relation_profil_apidae = """
                    DELETE FROM relation_profil_data_from_apidae 
                    WHERE id_relation_profil_apidae=%s; 
                    """
delete_relation_profil_apidae_with_id_data_from_apidae = """
                    DELETE FROM relation_profil_data_from_apidae 
                    WHERE id_data_from_apidae=%s; 
                    """
