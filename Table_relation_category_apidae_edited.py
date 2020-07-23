"""----------------------------
Creation date : 2020-07-22
Last update : 2020-07-22
----------------------------"""

drop_relation_category_apidae_edited = """
                                    DROP TABLE IF EXISTS category_apidae_edited CASCADE;
                                    """

relation_category_apidae_edited = """
                                    CREATE TABLE IF NOT EXISTS category_apidae_edited (
                                        id_category_apidae_edited SERIAL PRIMARY KEY,
                                        id_category BIGINT REFERENCES category ON DELETE CASCADE,
                                        id_data_from_apidae BIGINT REFERENCES data_from_apidae ON DELETE CASCADE
                                    )"""

insert_relation_category_apidae_edited = """
                                            INSERT INTO category_apidae_edited (
                                                id_category, id_data_from_apidae)
                                            VALUES (%s, %s) 
                                            returning id_category_apidae_mdified;
                                            """


delete_relation_category_apidae_edited = """
                                            DELETE FROM category_apidae_edited 
                                            WHERE id_category_apidae_edited=%s; 
                                            """

delete_relation_category_apidae_with_id_data_from_apidae_edited = """
                                                                    DELETE FROM category_apidae_edited 
                                                                    WHERE id_data_from_apidae=%s; 
                                                                    """
