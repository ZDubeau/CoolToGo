drop_admin = """
            DROP TABLE IF EXISTS administrators;
            """

admin = """
        CREATE TABLE IF NOT EXISTS administrators (
            id_admin BIGSERIAL PRIMARY KEY,
            admin_name TEXT NOT NULL,
            admin_pwd_hash TEXT,
            admin_email TEXT
        )"""

insert_admin = """
                INSERT INTO administrators (admin_name, admin_pwd_hash, admin_email)
                VALUES (%(admin_name)s, %(admin_pwd_hash)s, %(admin_email)s) 
                returning id_admin;
                """

nombre_admin = """
                SELECT count(*) 
                FROM administrators;
                """

select_id_admin = """
                    SELECT id_admin 
                    FROM administrators 
                    WHERE admin_name = %s;
                    """
select_admin = """
                SELECT admin_name 
                FROM administrators;
                """
select_password = """
                    SELECT admin_pwd_hash 
                    FROM administrators 
                    WHERE admin_name = %s;
                    """

select_admin_for_display = """
                            SELECT id_admin as id, admin_name as nom, admin_email as adresse_mail,'' as supprimer
                            FROM administrators 
                            ORDER BY id_admin ASC;
                            """

delete_admin = """
                DELETE 
                FROM administrators 
                WHERE id_admin=%s; 
                """
