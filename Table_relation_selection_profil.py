drop_relation_selection_profil = """
                                DROP TABLE IF EXISTS selection_profils_usager CASCADE;
                                """

relation_selection_profil = """
                            CREATE TABLE IF NOT EXISTS selection_profil (
                                id SERIAL PRIMARY KEY,
                                id_selection INTEGER REFERENCES selection ON DELETE CASCADE, 
                                id_profil INTEGER REFERENCES profil ON DELETE CASCADE
                            )"""

insert_relation_selection_profil = """
                                    INSERT INTO selection_profil (id_selection,id_profil)
                                    VALUES (%s,%s);
                                    """

delete_relation_selection_profil = """
                                    DELETE 
                                    FROM selection_profil
                                    WHERE id_selection=%s AND id_profil=%s; 
                                    """
