drop_relation_selection_profil = """
                                DROP TABLE IF EXISTS selection_profils_usager CASCADE;
                                """

relation_selection_profil = """
                            CREATE TABLE IF NOT EXISTS selection_profils_usager (
                                id SERIAL PRIMARY KEY,
                                id_selection INTEGER REFERENCES selection ON DELETE CASCADE, 
                                id_profil INTEGER REFERENCES profils_usager ON DELETE CASCADE, 
                            )"""
