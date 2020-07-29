""" ----------------------------
Creation date : 2020-07-08
Last update   : 2020-07-22
----------------------------"""

drop_manualEntry = """
                    DROP TABLE IF EXISTS manual_entry;
                    """

manualEntry = """
                CREATE TABLE IF NOT EXISTS manual_entry (
                  id_manual SERIAL PRIMARY KEY,
                  id_apidae BIGINT,
                  id_selection INTEGER REFERENCES selection ON DELETE CASCADE,
                  type_apidae VARCHAR(500),
                  titre VARCHAR(600),
                  profil_c2g VARCHAR(203),
                  categorie_c2g VARCHAR(601),
                  adresse1 TEXT,
                  adresse2 TEXT,
                  code_postal VARCHAR(20),
                  ville VARCHAR(200),
                  altitude TEXT,
                  latitude FLOAT,
                  longitude FLOAT,
                  telephone TEXT,
                  email VARCHAR(1004),
                  site_web TEXT,
                  description_courte TEXT,
                  description_detaillee TEXT,
                  image VARCHAR(400),
                  publics VARCHAR(1007),
                  tourisme_adapte VARCHAR(201),
                  payant BOOLEAN,
                  animaux_acceptes VARCHAR(1006),
                  environnement VARCHAR(1000),
                  equipement VARCHAR(1001),
                  services VARCHAR(1002),
                  periode VARCHAR(1003),
                  activites VARCHAR(1008),
                  ouverture TEXT,
                  date_debut DATE,
                  date_fin DATE,
                  typologie VARCHAR(1005),
                  bons_plans TEXT,
                  dispositions_speciales TEXT,
                  service_enfants TEXT,
                  service_cyclistes TEXT,
                  nouveaute_2020 TEXT
                )"""

insert_manualEntry = """
                    INSERT INTO manual_entry (
                      id_apidae, id_selection, type_apidae, titre, profil_c2g, categorie_c2g, adresse1,
                      adresse2, code_postal, ville, altitude, latitude, longitude, telephone, email,
                      site_web, description_courte, description_detaillee, image, publics, tourisme_adapte,
                      payant, animaux_acceptes, environnement, equipement, services, periode, activites,
                      ouverture, date_debut, date_fin, typologie, bons_plans, dispositions_speciales, 
                      service_enfants, service_cyclistes, nouveaute_2020)
                    VALUES (
                      %(id_apidae)s,%(id_selection)s, %(type_apidae)s, %(titre)s, %(profil_c2g)s,
                      %(categorie_c2g)s,%(adresse1)s, %(adresse2)s, %(code_postal)s, %(ville)s, %(altitude)s,
                      %(latitude)s, %(longitude)s, %(telephone)s, %(email)s, %(site_web)s, %(description_courte)s,
                      %(description_detaillee)s,%(image)s, %(Publics)s, %(tourisme_adapte)s,%(payant)s,
                      %(animaux_acceptes)s, %(environnement)s, %(equipement)s, %(services)s, %(periode)s,
                      %(activites)s, %(ouverture)s, %(date_debut)s, %(date_fin)s, %(typologie)s, %(bons_plans)s, 
                      %(dispositions_speciales)s, %(service_enfants)s, %(service_cyclistes)s, %(nouveaute_2020)s) 
                    returning id_manual;"""

update_manualEntry = """
                        UPDATE manual_entry 
                        SET id_apidae = %(id_apidae)s,
                            id_selection = %(id_selection)s,
                            type_apidae = %(type_apidae)s,
                            titre = %(titre)s,
                            profil_c2g = %(profil_c2g)s,
                            categorie_c2g = %(categorie_c2g)s,
                            Adresse1 = %(Adresse1)s,
                            Adresse2 = %(Adresse2)s, 
                            Code_postal =%(Code_postal)s, 
                            Ville = %(Ville)s,
                            telephone = %(telephone)s,
                            email = %(email)s,
                            site_web = %(site_web)s,
                            description_courte = %(description_courte)s, 
                            description_detaillee = %(description_detaillee)s, 
                            image =%(Images)s, 
                            Publics = %(Publics)s, 
                            tourisme_adapte =%(tourisme_adapte)s,
                            payant = %(payant)s,
                            animaux_acceptes = %(animaux_acceptes)s, 
                            environnement =%(environnement)s, 
                            equipement = %(equipement)s, 
                            services = %(services)s,
                            periode = %(periode)s,
                            activites = %(activites)s,
                            ouverture = %(ouverture)s,
                            Dates_début = %(Dates_début)s, 
                            Dates_fin =%(Dates_fin)s,
                            typologie = %(typologie)s,
                            bons_plans = %(bons_plans)s,
                            dispositions_speciales = %(dispositions_speciales)s,
                            service_enfants = %(service_enfants)s,
                            service_cyclistes = %(service_cyclistes)s,
                            nouveaute_2020 = %(nouveaute_2020)s
                        WHERE id_apidae = %(id_apidae)s 
                        returning id_manual;"""

select_id_manualEntry = """
  SELECT id AS id_me FROM manual_entry WHERE id_apidae = %s; """

select_manualEntry = """
  SELECT * FROM manual_entry; """

select_manualEntry_for_display = """
    SELECT *, '' as Edit, '' as Del FROM manual_entry ORDER BY id ASC; """

select_manualEntry_with_id = """
  SELECT * FROM manual_entry WHERE id=%s; """

select_max_id_from_manualEntry = """
  SELECT MAX(id) FROM manual_entry; """

delete_from_manualEntry_with_id = """
  DELETE FROM manual_entry WHERE id=%s; """
