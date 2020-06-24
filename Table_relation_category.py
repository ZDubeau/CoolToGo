drop_relation_selection_category = """
                                    DROP TABLE IF EXISTS selection_categories CASCADE;
                                    """

relation_selection_category = """
                                CREATE TABLE IF NOT EXISTS selection_categories (
                                    id SERIAL PRIMARY KEY,
                                    id_selection INTEGER REFERENCES selection ON DELETE CASCADE, 
                                    id_categorie INTEGER REFERENCES categories ON DELETE CASCADE, 
                                )"""
