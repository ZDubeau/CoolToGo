drop_relation_eltref_profil = """
                            DROP TABLE IF EXISTS eltref_profil;
                            """

relation_eltref_profil = """
                        CREATE TABLE IF NOT EXISTS eltref_profil (
                            id_eltref_prf SERIAL PRIMARY KEY,
                            id_profil BIGINT REFERENCES profil ON DELETE CASCADE,
                            id_eltref BIGINT REFERENCES elementreference ON DELETE CASCADE
                        )"""

insert_relation_eltref_profil = """
                                INSERT INTO eltref_profil (id_profil, id_eltref)
                                VALUES (%s,%s);
                                """

select_relation_eltref_profil = """
                                SELECT *
                                FROM eltref_profil; 
                                """

select_relation_eltref_profil_with_id = """
                                        SELECT *
                                        FROM eltref_profil
                                        WHERE id_eltref_prf=%s; 
                                        """

delete_relation_eltref_profil = """
                                DELETE 
                                FROM eltref_profil
                                WHERE id_eltref_prf=%s; 
                                """
