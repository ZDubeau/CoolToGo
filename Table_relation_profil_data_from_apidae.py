""" 
Projet CoolToGo
----------------------------
Creation date : 2020-06-11
Last update : 2020-07-13
----------------------------
"""

drop_relation_profil_apidae = """
                DROP TABLE IF EXISTS profil_apidae CASCADE;
                """

relation_profil_apidae = """
            CREATE TABLE IF NOT EXISTS profil_apidae (
                id_profil_apidae SERIAL PRIMARY KEY,
                id_profil BIGINT REFERENCES profil ON DELETE CASCADE,
                id_data_from_apidae BIGINT REFERENCES data_from_apidae ON DELETE CASCADE
            )"""

insert_relation_profil_apidae = """
                    INSERT INTO profil_apidae (id_profil, id_data_from_apidae)
                    VALUES (%s, %s) 
                    returning id_profil_apidae;
                    """


delete_relation_profil_apidae = """
                    DELETE FROM profil_apidae 
                    WHERE id_profil_apidae=%s; 
                    """
delete_relation_profil_apidae_with_id_data_from_apidae = """
                    DELETE FROM profil_apidae 
                    WHERE id_data_from_apidae=%s; 
                    """
