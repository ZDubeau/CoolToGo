drop_category = """
                DROP TABLE IF EXISTS category CASCADE;
                """

category = """
            CREATE TABLE IF NOT EXISTS category (
                id_category SERIAL PRIMARY KEY,
                category VARCHAR(100)
            )"""

insert_category = """
                INSERT INTO category (category)
                VALUES (%(category)s) 
                returning id_category;
                """

select_category = """
                        SELECT id_category as id, category as catégorie, '' as modifier, '' as supprimer
                        FROM category; 
                        """

select_category_with_id = """
                        SELECT id_category, category
                        FROM category 
                        WHERE id_category=%s; 
                        """

select_category_with_description = """
                                    SELECT * 
                                    FROM category 
                                    WHERE category=%(category)s
                                    """

update_category = """
                    UPDATE category 
                    SET category=%s 
                    WHERE id_category=%s;
                    """

delete_category = """
                        DELETE 
                        FROM category 
                        WHERE id_category=%s; 
                        """
