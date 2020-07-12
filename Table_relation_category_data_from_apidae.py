""" 
Projet CoolToGo
----------------------------
Creation date : 2020-06-11
Last update : 2020-07-11
----------------------------
"""

drop_relation_category_apidae = """
                                DROP TABLE IF EXISTS relation_category_data_from_apidae CASCADE;
                                """

relation_category_apidae = """
                            CREATE TABLE IF NOT EXISTS relation_category_data_from_apidae (
                                id_relation_category_apidae SERIAL PRIMARY KEY,
                                id_category BIGINT REFERENCES category ON DELETE CASCADE,
                                id_data_from_apidae BIGINT REFERENCES data_from_apidae ON DELETE CASCADE
                            )"""

insert_relation_category_apidae = """
                                    INSERT INTO relation_category_data_from_apidae (
                                        id_category, id_data_from_apidae)
                                    VALUES (%s, %s) 
                                    returning id_relation_category_apidae;
                                    """


delete_relation_category_apidae = """
                                    DELETE FROM relation_category_data_from_apidae 
                                    WHERE id_relation_category_apidae=%s; 
                                    """

delete_relation_category_apidae_with_id_data_from_apidae = """
                                                            DELETE FROM relation_category_data_from_apidae 
                                                            WHERE id_data_from_apidae=%s; 
                                                            """
