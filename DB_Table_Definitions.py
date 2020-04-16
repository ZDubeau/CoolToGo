""" Projet CoolToGo Alone """
############################################
""" Module by Zahra
𐤟 Création : 2020-03-06
𐤟 Dernière MàJ : 2020-04-13
"""

################ Tables des données extraites d'apidae ################

drop_cooltogo_from_apidae ="""DROP TABLE IF EXISTS cooltogo_from_apidae;"""

cooltogo_from_apidae = """
  CREATE TABLE IF NOT EXISTS cooltogo_from_apidae (
        id SERIAL PRIMARY KEY,
        id_apidae VARCHAR(50),
        id_selection BIGINT,
        lieu_event TEXT,
        names TEXT,
        types TEXT,
        latitude FLOAT,
        longitude FLOAT,
        adresse1 TEXT,
        adresse2 TEXT,
        code_postal VARCHAR(10),
        ville TEXT,
        telephone VARCHAR(20),
        email TEXT,
        site_web TEXT,
        description_teaser TEXT,
        images TEXT,
        publics TEXT,
        categories TEXT,
        accessibilité TEXT,
        payant BOOL,
        plus_d_infos_et_horaires TEXT,
        date_début DATE,
        date_fin DATE
    )"""

insert_cooltogo_from_apidae = """
  INSERT INTO cooltogo_from_apidae (id_apidae,id_selection, lieu_event, names, types, latitude, longitude, adresse1, adresse2, code_postal, ville,telephone, email, site_web, description_teaser, images, publics, categories, accessibilité, payant, plus_d_infos_et_horaires, date_début, date_fin)
  VALUES (%(id_apidae)s,%(id_selection)s, %(lieu_event)s, %(names)s, %(types)s, %(latitude)s, %(longitude)s, %(adresse1)s, %(adresse2)s, %(code_postal)s, %(ville)s, %(telephone)s, %(email)s, %(site_web)s, %(description_teaser)s, %(images)s, %(publics)s, %(categories)s, %(accessibilité)s, %(payant)s, %(plus_d_infos_et_horaires)s, %(date_début)s, %(date_fin)s) returning id;"""


################ Tables des données validés par l'administrateur ################

drop_cooltogo_validated ="""DROP TABLE IF EXISTS cooltogo_validated;"""

cooltogo_validated = """
  CREATE TABLE IF NOT EXISTS cooltogo_validated (
          id SERIAL PRIMARY KEY,
          id_apidae VARCHAR(50),
          Lieu_event TEXT,
          X FLOAT,
          Y FLOAT,
          name TEXT,
          Adresse1 TEXT,
          Adresse2 TEXT,
          Code_postal VARCHAR(10),
          Ville TEXT,
          telephone VARCHAR(20),
          email TEXT,
          site_web TEXT,
          Description_Teaser TEXT,
          Description TEXT,
          Images TEXT,
          Publics TEXT,
          styleUrl TEXT,
          styleHash TEXT,
          Type TEXT,
          Catégories TEXT,
          Accessibilité TEXT,
          payant BOOL,
          Plus_d_infos_et_horaires TEXT,
          Dates_début DATE,
          Dates_fin DATE
    )"""

insert_cooltogo_validated = """
  INSERT INTO cooltogo_validated (id_apidae,Lieu_event, X, Y, name, Adresse1, Adresse2, Code_postal, Ville, telephone, email, site_web, Description_Teaser, Description, Images, Publics, styleUrl, styleHash, Type, Catégories, Accessibilité, payant, Plus_d_infos_et_horaires, Dates_début, Dates_fin)
  VALUES (%(id_apidae)s, %(Lieu_event)s, %(X)s, %(Y)s, %(name)s, %(Adresse1)s, %(Adresse2)s, %(Code_postal)s, %(Ville)s, %(telephone)s, %(email)s, %(site_web)s, %(Description_Teaser)s, %(Description)s,%(Images)s, %(Publics)s, %(styleUrl)s, %(styleHash)s, %(Type)s, %(Catégories)s, %(Accessibilité)s, %(payant)s, %(Plus_d_infos_et_horaires)s, %(Dates_début)s, %(Dates_fin)s) returning id;"""

update_cooltogo_validated = """
  UPDATE cooltogo_validated 
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

################ Table des administrateurs ################

drop_administrators = """DROP TABLE IF EXISTS administrators;"""

administrators = """
  CREATE TABLE IF NOT EXISTS administrators (
        PKId_Admin BIGSERIAL PRIMARY KEY,
        Admin_Name TEXT NOT NULL,
        Admin_pwd_hash TEXT,
        Admin_email TEXT
  )"""

insert_administrators = """
  INSERT INTO administrators (Admin_Name, Admin_pwd_hash, Admin_email)
  VALUES (%(Admin_Name)s, %(Admin_pwd_hash)s, %(Admin_email)s) returning PKId_Admin;"""

#################### Tables des messages ###################

drop_message = """DROP TABLE IF EXISTS message;"""

message = """
  CREATE TABLE IF NOT EXISTS message (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL,
        published_on TIMESTAMP,
        active BOOL
    )"""

insert_message = """
  INSERT INTO message (message, published_on, active)
  VALUES (%(message)s, %(published_on)s, %(active)s) returning id;"""

################### Tables des selection ####################

drop_selection = """DROP TABLE IF EXISTS selection;"""

selection = """
    CREATE TABLE IF NOT EXISTS selection (
        id SERIAL PRIMARY KEY,
        selection TEXT NOT NULL,
        description TEXT NOT NULL,
        selection_type TEXT NOT NULL
    )"""

insert_selection = """
  INSERT INTO selection (selection, description, selection_type)
  VALUES (%(selection)s, %(description)s, %(selection_type)s) returning id;"""

################ Tables des selection extraction ################

drop_selection_extraction = """DROP TABLE IF EXISTS selection_extraction;"""

selection_extraction = """
    CREATE TABLE IF NOT EXISTS selection_extraction (
        id SERIAL PRIMARY KEY,
        selection_id BIGINT NOT NULL,
        selection_extraction_date TIMESTAMP NOT NULL,
        selection_extraction_nb_records BIGINT
    )"""

################ Tables des niveaux de fraicheurs ################

drop_niveau_de_fraicheur = """DROP TABLE IF EXISTS niveau_de_fraicheur;"""

niveau_de_fraicheur = """
    CREATE TABLE IF NOT EXISTS niveau_de_fraicheur (
        id SERIAL PRIMARY KEY,
        niveau_de_fraicheur TEXT NOT NULL,
        active BOOL NOT NULL DEFAULT TRUE
    )"""

insert_niveau_de_fraicheur = """
  INSERT INTO niveau_de_fraicheur (niveau_de_fraicheur)
  VALUES (%(niveau_de_fraicheur)s) returning id;"""

update_niveau_de_fraicheur ="""
  UPDATE niveau_de_fraicheur 
    SET niveau_de_fraicheur= %(niveau_de_fraicheur)s
        active = %(active)s
  WHERE id = %(id)s returning id;"""

################ Tables des liens niveaux de fraicheurs - lieux active ################

drop_lien_niveau_de_fraicheur_cooltogo_validated = """DROP TABLE IF EXISTS lien_niveau_de_fraicheur_cooltogo_validated;"""

lien_niveau_de_fraicheur_cooltogo_validated = """
    CREATE TABLE IF NOT EXISTS lien_niveau_de_fraicheur_cooltogo_validated (
        id SERIAL PRIMARY KEY,
        id_cooltogo_validated BIGINT,
        id_niveau_de_fraicheur BIGINT
    )"""

insert_lien_niveau_de_fraicheur_cooltogo_validated = """
  INSERT INTO lien_niveau_de_fraicheur_cooltogo_validated (id_cooltogo_validated, id_niveau_de_fraicheur)
  VALUES (%(id_cooltogo_validated)s, %(id_niveau_de_fraicheur)s) returning id;"""

update_lien_niveau_de_fraicheur_cooltogo_validated ="""
  UPDATE lien_niveau_de_fraicheur_cooltogo_validated 
    SET id_niveau_de_fraicheur= %(id_niveau_de_fraicheur)s
  WHERE id_cooltogo_validated = %(id_cooltogo_validated)s returning id;"""

delete_lien_niveau_de_fraicheur_cooltogo_validated ="""
DELETE FROM lien_niveau_de_fraicheur_cooltogo_validated 
WHERE id_cooltogo_validated = %(id_cooltogo_validated)s;"""

############################ THE END ################################