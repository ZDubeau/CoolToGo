drop_relation_eltref_prf = """
                            DROP TABLE IF EXISTS eltref_prf;
                            """

relation_eltref_prf = """
                    CREATE TABLE IF NOT EXISTS eltref_prf (
                        id_eltref_prf SERIAL PRIMARY KEY,
                        id_profil BIGINT REFERENCES profil ON DELETE CASCADE,
                        id_eltref BIGINT REFERENCES elementreference ON DELETE CASCADE
                    )"""

select_relation_eltref_prf = """
                                    SELECT *
                                    FROM eltref_prf; 
                                    """

insert_relation_eltref_prf = """
                            INSERT INTO eltref_prf (
                                id_profil, id_eltref)
                            VALUES (
                                %(id_profil)s, %(id_eltref)s)
                                returning id_eltref_prf;
                            """

select_relation_eltref_prf_with_id = """
                                    SELECT *
                                    FROM eltref_prf
                                    WHERE id_eltref_prf=%s; 
                                    """

delete_relation_eltref_prf = """
                            DELETE 
                            FROM eltref_prf
                            WHERE id_eltref_prf=%s; 
                            """
