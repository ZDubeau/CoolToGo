drop_themDescrip = """
                    DROP TABLE IF EXISTS themedDescription;
                    """

themDescrip = """
                CREATE TABLE IF NOT EXISTS themedDescription (
                    id_themDsc SERIAL PRIMARY KEY,
                    id_apidae BIGINT,
                    id_eltRef BIGINT REFERENCES elementReference ON DELETE CASCADE,
                    description TEXT
            )"""

insert_themDescrip = """
                    INSERT INTO themedDescription (
                        id_apidae, id_eltRef, description)
                    VALUES (
                        %(id_apidae)s, %(id_eltRef)s, %(description)s)
                        returning id_themDsc;
                    """

select_themDescrip_with_id = """
                            SELECT *
                            FROM themedDescription
                            WHERE id_themDsc=%s; 
                            """

delete_themDescrip = """
                    DELETE 
                    FROM themedDescription
                    WHERE id_themDsc=%s; 
                    """
