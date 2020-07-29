"""----------------------------
Creation date : 2020-06-11
Last update : 2020-07-29
----------------------------"""

drop_category = """
                DROP TABLE IF EXISTS category CASCADE;
                """

category = """
            CREATE TABLE IF NOT EXISTS category (
                id_category SERIAL PRIMARY KEY,
                category_name VARCHAR(100)
            )"""

insert_category = """
                    INSERT INTO category (category_name)
                    VALUES (%(category_name)s) 
                    returning id_category;
                    """

select_category = """
                    SELECT id_category AS id, category_name AS catégories, '' AS modifier, '' AS supprimer
                    FROM category
                    ORDER BY id_category ASC; 
                    """

select_category_for_selection_id = """
                                    SELECT c.id_category AS id, c.category_name AS catégories, sc.id AS link
                                    FROM category AS c 
                                    LEFT JOIN (
                                        SELECT * 
                                        FROM selection_category 
                                        WHERE id_selection=%s) AS sc 
                                    ON c.id_category=sc.id_category; 
                                    """

select_category_for_apidae_id = """
                                SELECT c.id_category AS id, c.category_name AS catégories, ac.id AS relation
                                FROM category AS c 
                                LEFT JOIN (
                                    SELECT * 
                                    FROM category_apidae_edited
                                    WHERE id_data_from_apidae=%s) AS ac 
                                ON c.id_category=ac.id_category; 
                                """

select_category_with_id = """
                            SELECT id_category, category_name
                            FROM category 
                            WHERE id_category=%s; 
                            """

select_category_with_description = """
                                    SELECT * 
                                    FROM category 
                                    WHERE category_name=%(category_name)s
                                    """

update_category = """
                    UPDATE category 
                    SET category_name=%s 
                    WHERE id_category=%s;
                    """

delete_category = """
                    DELETE 
                    FROM category 
                    WHERE id_category=%s; 
                    """
