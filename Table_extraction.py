"""----------------------------
Creation date : 2020-06-30
Last update : 2020-07-29
----------------------------"""

drop_selection_extraction = """
                            DROP TABLE IF EXISTS selection_extraction CASCADE;
                            """

selection_extraction = """
                        CREATE TABLE IF NOT EXISTS selection_extraction (
                            id SERIAL PRIMARY KEY,
                            id_selection INTEGER REFERENCES selection ON DELETE CASCADE,
                            selection_extraction_date TIMESTAMP NOT NULL,
                            selection_extraction_nb_records BIGINT
                        )"""

insert_selection_extraction = """
                                INSERT INTO selection_extraction (
                                    id_selection,selection_extraction_date,selection_extraction_nb_records) 
                                VALUES (
                                    %s,NOW(),%s);
                                """
