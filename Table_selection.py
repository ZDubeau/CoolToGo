drop_selection = """
                    DROP TABLE IF EXISTS selection CASCADE;
                    """

selection = """
            CREATE TABLE IF NOT EXISTS selection (
                id_selection SERIAL PRIMARY KEY,
                id_project INTEGER REFERENCES project ON DELETE CASCADE,
                selection TEXT NOT NULL,
                description TEXT NOT NULL
            )"""

insert_selection = """
                    INSERT INTO selection (
                        id_project,selection, description)
                    VALUES (
                        %(id_project)s, %(selection)s, %(description)s) 
                    returning id_selection;
                    """

select_selection_with_id = """
                            SELECT selection,description,id_project 
                            FROM selection 
                            WHERE id_selection=%s; 
                            """

select_selection_with_type = """
                            SELECT id_selection
                            FROM selection 
                            WHERE selection=%s; 
                            """

select_selection_information = """
                                SELECT s.id_selection as id, p.project_ID as id_projet, s.selection as id_selection, s.description as selection, se.selection_extraction_date AS dernier_extract, se.selection_extraction_nb_records AS Nb_records, '' as lancement
                                FROM selection AS s 
                                LEFT JOIN project AS p 
                                ON s.id_project=p.id_project 
                                LEFT OUTER JOIN selection_extraction AS se 
                                ON s.id_selection = se.id_selection 
                                AND se.selection_extraction_date =(
                                    SELECT MAX(selection_extraction_date) 
                                    FROM selection_extraction 
                                    WHERE id_selection=se.id_selection);
                                """

delete_selection_with_project_id = """
                                    DELETE 
                                    FROM selection 
                                    WHERE id_project=%s; 
                                    """

delete_selection = """
                    DELETE 
                    FROM selection 
                    WHERE id_selection=%s; 
                    """
