drop_relation_eltref_profil = """
                            DROP TABLE IF EXISTS eltref_profil CASCADE;
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
                                SELECT ep.id_eltref_prf,ep.id_profil, er.id_elref_in_apidae, er.description,'' as Supprimer
                                FROM eltref_profil as ep
                                LEFT JOIN elementreference as er
                                ON ep.id_eltref = er.id_eltref
                                WHERE id_profil = %(id_profil)s; 
                                """

select_relation_eltref_profil_with_id = """
                                        SELECT *
                                        FROM eltref_profil
                                        WHERE id_eltref_prf=%s; 
                                        """

select_relation_eltref_profil_with_profil_element_reference = """
                                                                SELECT id_eltref_prf
                                                                FROM eltref_profil
                                                                WHERE id_profil=%s AND id_eltref=%s; 
                                                                """

delete_relation_eltref_profil = """
                                DELETE 
                                FROM eltref_profil
                                WHERE id_eltref_prf=%s; 
                                """
