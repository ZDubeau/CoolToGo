drop_freshness_level = """
                        DROP TABLE IF EXISTS freshness CASCADE;
                        """

freshness_level = """
                    CREATE TABLE IF NOT EXISTS freshness (
                        id_fresh SERIAL PRIMARY KEY,
                        freshness TEXT NOT NULL,
                        score_freshness INTEGER NOT NULL,
                        active BOOL NOT NULL DEFAULT TRUE
                    )"""

insert_freshness_level = """
                        INSERT INTO freshness (freshness, score_freshness)
                        VALUES (%s, %s) returning id_fresh;
                        """

select_freshness_level_for_diplay = """
                                    SELECT id_fresh,freshness AS fraîcheur, score_freshness AS Note,'' as état, '' AS Changer 
                                    FROM freshness;
                                    """

select_all_freshness_level = """
                            SELECT id_fresh, freshness 
                            FROM freshness 
                            WHERE active 
                            ORDER BY freshness ASC;
                            """

update_freshness_level = """
                        UPDATE freshness 
                        SET freshness= %(freshness)s
                            active = %(active)s
                        WHERE id_fresh = %(id)s returning id_fresh;
                        """

change_freshness_level_status = """
                                UPDATE freshness 
                                SET active = NOT active 
                                WHERE id_fresh =%s; 
                                """
