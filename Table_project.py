drop_project = """
              DROP TABLE IF EXISTS project CASCADE;
              """

project = """
            CREATE TABLE IF NOT EXISTS project (
                id_project SERIAL PRIMARY KEY,
                project_ID TEXT NOT NULL,
                api_key TEXT NOT NULL
            )"""

insert_project = """
                INSERT INTO project (project_ID, api_key)
                VALUES (%(project_ID)s, %(api_key)s) 
                returning id_project;
                """

select_project_with_id = """
                        SELECT project_ID, api_key 
                        FROM project 
                        WHERE id_project=%s; 
                        """

select_project_information = """
                            SELECT id_project, project_ID as id_project, api_key,'' as lancement, '' as supprimer
                            FROM project; 
                            """

select_selection_project = """
                            SELECT project_ID, api_key,selection 
                            FROM project as p 
                            LEFT JOIN selection as s 
                            ON p.id_project=s.id_project
                            WHERE s.id_selection=%s; 
                            """

delete_project_with_id = """
                        DELETE 
                        FROM project 
                        WHERE id_project=%s; 
                        """
