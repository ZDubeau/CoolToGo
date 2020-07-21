drop_user_profil = """
                    DROP TABLE IF EXISTS profil CASCADE;
                    """

user_profil = """
                CREATE TABLE IF NOT EXISTS profil (
                    id_profil SERIAL PRIMARY KEY,
                    profil VARCHAR(80),
                    basic BOOLEAN DEFAULT TRUE,
                    icon_ctg VARCHAR(100),
                    icon_type VARCHAR(100)
                )"""

insert_user_profil = """
                    INSERT INTO profil (profil)
                    VALUES (%(profil)s) 
                    returning id_profil;
                    """

select_user_profil = """
                    SELECT id_profil as id, profil as profil_usagers, basic, '' as modifier, '' as supprimer
                    FROM profil;
                    """
select_basic_user_profil = """
                    SELECT id_profil as id
                    FROM profil WHERE basic;
                    """

select_profil_for_selection_id = """
                                SELECT p.id_profil AS id, p.profil AS profil_usagers, sp.id AS link
                                FROM profil AS p 
                                LEFT JOIN (
                                    SELECT * 
                                    FROM selection_profil 
                                    WHERE id_selection=%s) AS sp 
                                ON p.id_profil=sp.id_profil; 
                                """

select_user_profil_with_id = """
                                SELECT id_profil, profil
                                FROM profil
                                WHERE id_profil=%s; 
                            """

select_user_profil_with_description = """
                                        SELECT * 
                                        FROM profil
                                        WHERE profil=%(profil)s
                                    """

update_user_profil = """
                        UPDATE profil
                        SET profil=%s 
                        WHERE id_profil=%s;
                    """

delete_user_profil = """
                        DELETE 
                        FROM profil
                        WHERE id_profil=%s; 
                    """
