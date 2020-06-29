drop_elementRef = """
                    DROP TABLE IF EXISTS elementReference;
                    """

elementRef = """
             CREATE TABLE IF NOT EXISTS elementReference (
                id_eltRef SERIAL PRIMARY KEY,
                id_elRef_in_apidae BIGINT,
                description TEXT
            )"""

insert_elementRef = """
                    INSERT INTO elementReference (
                        id_elRef_in_apidae, description)
                    VALUES (
                        %(id_eltRef_in_apidae)s, %(description)s)
                        returning id_eltRef;
                    """

select_elementRef_with_id = """
                            SELECT *
                            FROM elementReference 
                            WHERE id_eltRef=%s; 
                            """

delete_elementRef = """
                    DELETE 
                    FROM elementReference 
                    WHERE id_eltRef=%s; 
                    """
