drop_relation_eltref_category = """
                                DROP TABLE IF EXISTS eltref_category;
                                """

relation_eltref_category = """
                            CREATE TABLE IF NOT EXISTS eltref_category (
                                id_eltref_ctg SERIAL PRIMARY KEY,
                                id_category BIGINT REFERENCES category ON DELETE CASCADE,
                                id_eltref BIGINT REFERENCES elementreference ON DELETE CASCADE
                            )"""

insert_relation_eltref_category = """
                                    INSERT INTO eltref_category (
                                        id_category, id_eltref)
                                    VALUES (
                                        %(id_category)s, %(id_eltref)s)
                                        returning id_eltref_ctg;
                                    """

select_relation_eltref_category_with_id = """
                                        SELECT *
                                        FROM eltref_category
                                        WHERE id_eltref_ctg=%s; 
                                        """

delete_relation_eltref_category = """
                                    DELETE 
                                    FROM eltref_category
                                    WHERE id_eltref_ctg=%s; 
                                    """
