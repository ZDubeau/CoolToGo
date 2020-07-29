drop_relation_selection_category = """
                                    DROP TABLE IF EXISTS selection_category CASCADE;
                                    """

relation_selection_category = """
                                CREATE TABLE IF NOT EXISTS selection_category (
                                    id SERIAL PRIMARY KEY,
                                    id_selection INTEGER REFERENCES selection ON DELETE CASCADE, 
                                    id_category INTEGER REFERENCES category ON DELETE CASCADE
                                )"""

insert_relation_selection_category = """
                                    INSERT INTO selection_category (id_selection,id_category)
                                    VALUES (%s,%s);
                                    """

delete_relation_selection_category = """
                                    DELETE 
                                    FROM selection_category
                                    WHERE id_selection=%s AND id_category=%s; 
                                    """
