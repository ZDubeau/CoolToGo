drop_user_profil = """
                    DROP TABLE IF EXISTS profils_usager CASCADE;
                    """

user_profil = """
                CREATE TABLE IF NOT EXISTS profils_usager (
                    id_profil SERIAL PRIMARY KEY,
                    profils VARCHAR(20)
                )"""

insert_user_profil = """
                INSERT INTO profils_usager (profils)
                VALUES (%(profils)s) 
                returning id_profil;
                """

delete_user_profil_with_id = """
                            DELETE 
                            FROM profils_usager 
                            WHERE id_profil=%s; 
                            """
