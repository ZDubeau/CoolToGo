""" 
Projet CoolToGo
----------------------------
Creation date : 2020-06-11
Last update : 2020-06-20
----------------------------
"""

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
                    SELECT id_category as id, category_name as catégories, '' as modifier, '' as supprimer
                    FROM category; 
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
