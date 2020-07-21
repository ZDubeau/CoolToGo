""" ----------------------------
Creation date : 2020-07-08
Last update   : 2020-07-21
----------------------------"""

drop_manualEntry = """DROP TABLE IF EXISTS manual_entry;"""

manualEntry = """
                CREATE TABLE IF NOT EXISTS manual_entry (
                    id SERIAL PRIMARY KEY,
                    category_c2g VARCHAR(500),
                    type_c2g VARCHAR(300),
                    title VARCHAR(600),
                    address TEXT,
                    code_postal VARCHAR(10),
                    city TEXT,
                    altitude VARCHAR(10),
                    lat FLOAT,
                    lng FLOAT,
                    tel VARCHAR(70),
                    mail TEXT,
                    url TEXT,
                    profil_c2g VARCHAR(150),
                    accessibility VARCHAR(170),
                    paying VARCHAR(4),
                    image TEXT,
                    opening TEXT,
                    date_start DATE,
                    date_end DATE,
                    description TEXT,
                    environment TEXT
                )"""

insert_manualEntry = """
                    INSERT INTO manual_entry (
                        category_c2g,type_c2g,title, address, code_postal, 
                        city, altitude, lat, lng, tel, mail, url, profil_c2g,
                        accessibility, paying, image, opening, date_start, date_end, 
                        description, environment)
                    VALUES (
                        %(category_c2g)s, %(type_c2g)s, %(title)s, %(address)s, 
                        %(code_postall)s, %(city)s, %(altitude)s, %(lat)s, %(lng)s,
                        %(tel)s, %(mail)s, %(url)s, %(profil_c2g)s, %(accessibility)s,
                        %(paying)s, %(image)s, %(opening)s, %(date_start)s,, %(date_end)s,
                        %(Description)s, %(environment)s) 
                    returning id;"""

update_manualEntry = """
                        UPDATE manual_entry 
                        SET  Lieu_event = %(Lieu_event)s,
                            X = %(X)s,
                            Y = %(Y)s,
                            name = %(name)s,
                            Adresse1 = %(Adresse1)s,
                            Adresse2 = %(Adresse2)s, 
                            Code_postal =%(Code_postal)s, 
                            Ville = %(Ville)s,
                            telephone = %(telephone)s,
                            email = %(email)s,
                            site_web = %(site_web)s,
                            Description_Teaser = %(Description_Teaser)s, 
                            Description = %(Description)s, 
                            Images =%(Images)s, 
                            Publics = %(Publics)s, 
                            styleUrl =%(styleUrl)s, 
                            styleHash = %(styleHash)s, 
                            Type =%(Type)s, 
                            Catégories = %(Catégories)s, 
                            Accessibilité = %(Accessibilité)s, 
                            payant = %(payant)s, 
                            Plus_d_infos_et_horaires = %(Plus_d_infos_et_horaires)s, 
                            Dates_début = %(Dates_début)s, 
                            Dates_fin =%(Dates_fin)s
                        WHERE id_apidae = %(id_apidae)s returning id;"""

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
