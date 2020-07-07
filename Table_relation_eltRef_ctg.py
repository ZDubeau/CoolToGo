drop_relation_eltRef_ctg = """
                            DROP TABLE IF EXISTS eltRef_ctg;
                            """

relation_eltRef_ctg = """
                    CREATE TABLE IF NOT EXISTS eltRef_ctg (
                        id_eltRef_ctg SERIAL PRIMARY KEY,
                        id_category BIGINT REFERENCES category ON DELETE CASCADE,
                        id_eltRef BIGINT REFERENCES elementReference ON DELETE CASCADE
                    )"""

insert_relation_eltRef_ctg = """
                            INSERT INTO eltRef_ctg (
                                id_category, id_eltRef)
                            VALUES (
                                %(id_category)s, %(id_eltRef)s)
                                returning id_eltRef_ctg;
                            """

select_relation_eltRef_ctg_with_id = """
                                    SELECT *
                                    FROM eltRef_ctg
                                    WHERE id_eltRef_ctg=%s; 
                                    """

delete_relation_eltRef_ctg = """
                            DELETE 
                            FROM eltRef_ctg
                            WHERE id_eltRef_ctg=%s; 
                            """
