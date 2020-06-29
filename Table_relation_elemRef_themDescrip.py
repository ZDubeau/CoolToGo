drop_relation_eltRef_themDscrip = """
                                    DROP TABLE IF EXISTS eltRef_themDsc;
                                    """

relation_eltRef_themDscrip = """
                            CREATE TABLE IF NOT EXISTS eltRef_themDsc (
                                id_eltRef_themDsc SERIAL PRIMARY KEY,
                                id_eltRef BIGINT REFERENCES elementReference ON DELETE CASCADE
                            )"""

insert_relation_eltRef_themDscrip = """
                                    INSERT INTO eltRef_themDsc (
                                        id_eltRef_themDsc)
                                    VALUES (
                                        %(id_eltRef_themDsc)s) 
                                    returning id_eltRef_themDsc;
                                    """

select_relation_eltRef_themDscrip_with_id = """
                                            SELECT id_eltRef_themDsc
                                            FROM eltRef_themDsc
                                            WHERE id_eltRef=%s; 
                                            """

delete_relation_eltRef_themDscrip = """
                                    DELETE 
                                    FROM eltRef_themDsc
                                    WHERE id_eltRef_themDsc=%s; 
                                    """
