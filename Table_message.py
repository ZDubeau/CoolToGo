drop_message = """
                DROP TABLE IF EXISTS message;
                """

message = """
            CREATE TABLE IF NOT EXISTS message (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                start_date DATE,
                end_date DATE
            )"""

insert_message = """
                INSERT INTO message (message, start_date, end_date)
                VALUES (%s,%s,%s) 
                returning id;
                """

select_message = """ 
                SELECT * 
                FROM message 
                WHERE id=%s;
                """

select_message_list = """ 
                        SELECT id,message, start_date, end_date, '' as Modifier, '' as Publier, '' as Supprimer 
                        FROM message; 
                        """

update_message = """
                UPDATE message 
                SET message=%s, start_date=%s, end_date=%s 
                WHERE id=%s;
                """

delete_message = """
                DELETE 
                FROM message 
                WHERE id=%s;
                """
