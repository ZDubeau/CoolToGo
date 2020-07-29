"""----------------------------
Creation date : 2020-07-22
Last update : 2020-07-22
----------------------------"""

drop_relation_profil_apidae_edited = """
                                    DROP TABLE IF EXISTS profil_apidae_edited CASCADE;
                                    """

relation_profil_apidae_edited = """
                                CREATE TABLE IF NOT EXISTS profil_apidae_edited (
                                    id SERIAL PRIMARY KEY,
                                    id_profil INTEGER REFERENCES profil ON DELETE CASCADE,
                                    id_data_from_apidae INTEGER REFERENCES data_from_apidae ON DELETE CASCADE
                                )"""

insert_relation_profil_apidae_edited = """
                                        INSERT INTO profil_apidae_edited (
                                            id_profil, id_data_from_apidae)
                                        VALUES (%s, %s) 
                                        returning id;
                                        """

delete_relation_profil_apidae_edited = """
                                        DELETE FROM profil_apidae_edited 
                                        WHERE id_profil=%s AND  id_data_from_apidae=%s; 
                                        """

delete_relation_profil_apidae_with_id_data_from_apidae_edited = """
                                                                DELETE FROM profil_apidae_edited 
                                                                WHERE id_data_from_apidae=%s; 
                                                                """
