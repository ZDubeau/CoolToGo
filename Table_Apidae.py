""" 
Projet CoolToGo
----------------------------
𐤟 Creation date : 2020-06-11
𐤟 Last update : 2020-06-19
Estimate time : 60 minutes
PASSED TIME UNTIL NOW: 1H
----------------------------
"""
# _______________________________________________________________________

drop_apidae = """
                DROP TABLE IF EXISTS data_from_apidae CASCADE;
                """
# selection TEXT REFERENCES selection ON DELETE CASCADE,
apidae = """
        CREATE TABLE IF NOT EXISTS data_from_apidae (
            id SERIAL PRIMARY KEY,
            id_apidae BIGINT,
            id_selection INTEGER REFERENCES selection ON DELETE CASCADE,
            type_apidae VARCHAR(500),
            titre VARCHAR(600),
            adresse1 TEXT,
            adresse2 TEXT,
            code_postal VARCHAR(10),
            ville VARCHAR(200),
            altitude TEXT,
            latitude FLOAT,
            longitude FLOAT,
            telephone VARCHAR(20),
            email VARCHAR(1004),
            site_web TEXT,
            description_courte TEXT,
            description_detaillee TEXT,
            image VARCHAR(400),
            publics VARCHAR(1007),
            tourisme_adapte VARCHAR(201),
            payant VARCHAR(3),
            animaux_acceptes VARCHAR(1006),
            environnement VARCHAR(1000),
            equipement VARCHAR(1001),
            services VARCHAR(1002),
            periode VARCHAR(1003),
            activites VARCHAR(1008),
            ouverture TEXT,
            typologie VARCHAR(1005)
        )"""

insert_apidae = """
                INSERT INTO data_from_apidae (
                    id_apidae,id_selection, type_apidae, titre, types,adresse1, adresse2, code_postal, 
                    ville, altitude, latitude, longitude, telephone, email, site_web, description_courte, 
                    description_detaillee, image, publics, tourisme_adapte, payant, animaux_acceptes,
                    environnement, equipement, services, periode, activites, ouverture, typologie)
                VALUES (
                    %(id_apidae)s,%(id_selection)s, %(type_apidae)s, %(titre)s, 
                    %(types)s, %(adresse1)s, %(adresse2)s, %(code_postal)s, %(ville)s, %(altitude)s,
                    %(latitude)s, %(longitude)s, %(telephone)s, %(email)s, %(site_web)s,
                    %(description_courte)s,%(description_detaillee)s,%(image)s, %(Publics)s,
                    %(tourisme_adapte)s,%(payant)s, %(animaux_acceptes)s, %(environnement)s,
                    %(equipement)s, %(services)s, %(periode)s, %(activites)s, %(ouverture)s, %(typologie)s) 
                returning id;
                """

select_apidae_display = """
                        SELECT * 
                        FROM data_from_apidae 
                        ORDER BY id ASC; 
                        """

select_apidae_1_id = """
                        SELECT * 
                        FROM data_from_apidae 
                        WHERE id=%s;
                        """

delete_apidae_selection_id = """
                                DELETE 
                                FROM data_from_apidae 
                                WHERE id_selection=%s; 
                                """

delete_apidae_project_id = """
                            DELETE 
                            FROM data_from_apidae 
                            WHERE id_selection IN (
                                SELECT id 
                                FROM selection 
                                WHERE id_projet=%s); 
                            """
