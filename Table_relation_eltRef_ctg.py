drop_relation_eltref_ctg = """
                            DROP TABLE IF EXISTS eltref_ctg;
                            """

relation_eltref_ctg = """
                    CREATE TABLE IF NOT EXISTS eltref_ctg (
                        id_eltref_ctg SERIAL PRIMARY KEY,
                        id_category BIGINT REFERENCES category ON DELETE CASCADE,
                        id_eltref BIGINT REFERENCES elementreference ON DELETE CASCADE
                    )"""

insert_relation_eltref_ctg = """
                            INSERT INTO eltref_ctg (
                                id_category, id_eltref)
                            VALUES (
                                %(id_category)s, %(id_eltref)s)
                                returning id_eltref_ctg;
                            """

select_relation_eltref_ctg_with_id = """
                                    SELECT *
                                    FROM eltref_ctg
                                    WHERE id_eltref_ctg=%s; 
                                    """

delete_relation_eltref_ctg = """
                            DELETE 
                            FROM eltref_ctg
                            WHERE id_eltref_ctg=%s; 
                            """
