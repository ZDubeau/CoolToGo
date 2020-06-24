drop_relation_selection_freshness = """
                                    DROP TABLE IF EXISTS selection_fraicheur CASCADE;
                                    """

relation_selection_freshness = """
                                CREATE TABLE IF NOT EXISTS selection_fraicheur (
                                    id SERIAL PRIMARY KEY,
                                    id_selection INTEGER REFERENCES selection ON DELETE CASCADE, 
                                    id_fraicheur INTEGER REFERENCES niveau_de_fraicheur ON DELETE CASCADE, 
                                )"""
