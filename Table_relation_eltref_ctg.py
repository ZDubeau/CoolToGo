drop_relation_eltref_category = """
                                DROP TABLE IF EXISTS eltref_category CASCADE;
                                """

relation_eltref_category = """
                            CREATE TABLE IF NOT EXISTS eltref_category (
                                id_eltref_ctg SERIAL PRIMARY KEY,
                                id_category BIGINT REFERENCES category ON DELETE CASCADE,
                                id_eltref BIGINT REFERENCES elementreference ON DELETE CASCADE
                            )"""

insert_relation_eltref_category = """
                                    INSERT INTO eltref_category (id_category, id_eltref)
                                    VALUES (%s, %s)
                                        returning id_eltref_ctg;
                                    """

select_relation_eltref_category = """
                                SELECT ec.id_eltref_ctg, ec.id_category, er.id_elref_in_apidae, er.description,'' as Supprimer
                                FROM eltref_category as ec
                                LEFT JOIN elementreference as er
                                ON ec.id_eltref = er.id_eltref
                                WHERE id_category = %(id_category)s;
                                """

select_relation_eltref_category_with_id = """
                                        SELECT *
                                        FROM eltref_category
                                        WHERE id_eltref_ctg=%s;
                                        """

select_relation_eltref_category_with_category_element_reference = """
                                        SELECT id_eltref_ctg
                                        FROM eltref_category
                                        WHERE id_category=%s AND id_eltref=%s;
                                        """

delete_relation_eltref_category = """
                                    DELETE
                                    FROM eltref_category
                                    WHERE id_eltref_ctg = %s;
                                    """
