""" Projet CoolToGo Alone """
############################################
""" Module by Zahra
𐤟 Création : 2020-03-06
𐤟 Dernière MàJ : 2020-04-13
"""

################ Tables des données extraites d'apidae ################

drop_cooltogo_from_apidae = """DROP TABLE IF EXISTS cooltogo_from_apidae;"""

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
        telephone TEXT,
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

select_cooltogo_from_apidae_for_display = """
  SELECT *,'' as a 
  FROM cooltogo_from_apidae 
  WHERE id_apidae NOT IN (SELECT DISTINCT id_apidae FROM cooltogo_validated) ORDER BY id ASC; """

select_cooltogo_from_apidae_one_id = """
  SELECT * FROM cooltogo_from_apidae WHERE id=%s; """

delete_cooltogo_from_apidae_with_selection_id = """
  DELETE FROM cooltogo_from_apidae WHERE id_selection=%s; """

delete_cooltogo_from_apidae_with_project_id = """
  DELETE FROM cooltogo_from_apidae WHERE id_selection IN (SELECT id FROM selection WHERE id_projet=%s); """

################ Tables des données validés par l'administrateur ################

drop_cooltogo_validated = """DROP TABLE IF EXISTS cooltogo_validated;"""

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

select_id_cooltogo_validated = """
  SELECT id AS id_valide FROM cooltogo_validated WHERE id_apidae = %s; """

select_cooltogo_validated = """
  SELECT * FROM cooltogo_validated; """

select_cooltogo_validated_for_display = """
    SELECT *, '' as Edit, '' as Del FROM cooltogo_validated ORDER BY id ASC; """

select_cooltogo_validate_with_id = """
  SELECT * FROM cooltogo_validated WHERE id=%s; """

select_max_id_from_cooltogo_validated = """
  SELECT MAX(id) FROM cooltogo_validated; """

delete_from_cooltogo_validated_with_id = """
  DELETE FROM cooltogo_validated WHERE id=%s; """

################ Table des administrateurs ################

# drop_administrators = """
#                       DROP TABLE IF EXISTS administrators;
#                       """

# administrators = """
#                 CREATE TABLE IF NOT EXISTS administrators (
#                   PKId_Admin BIGSERIAL PRIMARY KEY,
#                   Admin_Name TEXT NOT NULL,
#                   Admin_pwd_hash TEXT,
#                   Admin_email TEXT
#                 )"""

# insert_administrators = """
#                         INSERT INTO administrators (Admin_Name, Admin_pwd_hash, Admin_email)
#                         VALUES (%(Admin_Name)s, %(Admin_pwd_hash)s, %(Admin_email)s)
#                         returning PKId_Admin;
#                         """

# nombre_administrators = """
#   SELECT count(*) FROM administrators; """

# select_adminitrators_for_display = """
#   SELECT PKId_Admin as Id, Admin_Name as Name, Admin_email as Email,'' as Action FROM administrators ORDER BY PKId_Admin ASC;"""

# delete_administrators = """
#   DELETE FROM administrators WHERE PKId_Admin=%s; """

#################### Tables des messages ###################

# drop_message = """DROP TABLE IF EXISTS message;"""

# message = """
#   CREATE TABLE IF NOT EXISTS message (
#         id SERIAL PRIMARY KEY,
#         message TEXT NOT NULL,
#         start_date DATE,
#         end_date DATE
#     )"""

# insert_message = """
#   INSERT INTO message (message, start_date, end_date)
#   VALUES (%s,%s,%s) returning id;"""

# update_message = """
#   UPDATE message SET message=%s, start_date=%s, end_date=%s WHERE id=%s;"""

# delete_message = """
#   DELETE FROM message WHERE id=%s;"""

# select_message = """
#   SELECT * FROM message WHERE id=%s;"""

# select_message_list = """
#   SELECT id,message, start_date, end_date, '' as Edit, '' as Publish, '' as Delete FROM message; """

################### Tables des selection ####################

# drop_selection = """DROP TABLE IF EXISTS selection;"""

# selection = """
#     CREATE TABLE IF NOT EXISTS selection (
#         id SERIAL PRIMARY KEY,
#         id_projet BIGINT NULL,
#         selection TEXT NOT NULL,
#         description TEXT NOT NULL,
#         selection_type TEXT NOT NULL
#     )"""

# insert_selection = """
#   INSERT INTO selection (id_projet,selection, description, selection_type)
#   VALUES (%(id_project)s, %(selection)s, %(description)s, %(selection_type)s) returning id;"""

# edit_selection = """
#   UPDATE selection SET selection_type= %(selection_type)s WHERE id=%(id)s;"""

# select_selection_with_id = """
#   SELECT selection,description,selection_type,id_projet FROM selection WHERE id=%s; """

# select_selection_with_type = """
#   SELECT id, selection_type FROM selection WHERE selection=%s; """

# delete_selection_with_project_id = """
#   DELETE FROM selection WHERE id_projet=%s; """

# delete_selection = """
#   DELETE FROM selection WHERE id=%s; """

################ Tables des selection extraction ################

drop_selection_extraction = """DROP TABLE IF EXISTS selection_extraction;"""

selection_extraction = """
    CREATE TABLE IF NOT EXISTS selection_extraction (
        id SERIAL PRIMARY KEY,
        selection_id BIGINT NOT NULL,
        selection_extraction_date TIMESTAMP NOT NULL,
        selection_extraction_nb_records BIGINT
    )"""

insert_selection_extraction = """
  INSERT INTO selection_extraction (selection_id,selection_extraction_date,selection_extraction_nb_records) VALUES (%s,NOW(),%s);"""


select_selection_information = """
  SELECT s.id as id, p.project_ID as project_ID, s.selection as selection, s.description as categories, s.selection_type as Lieu_Event, se.selection_extraction_date AS Last_Extract, se.selection_extraction_nb_records AS Nb_records, '' as Launch, '' as Edit  
    FROM selection AS s LEFT JOIN projet AS p on s.id_projet=p.id LEFT OUTER JOIN selection_extraction AS se ON s.id = se.selection_id AND se.selection_extraction_date =(SELECT MAX(selection_extraction_date) FROM selection_extraction WHERE selection_id=se.selection_id);"""


################ Tables des niveaux de fraicheurs ################

drop_niveau_de_fraicheur = """
                            DROP TABLE IF EXISTS niveau_de_fraicheur;
                            """

niveau_de_fraicheur = """
                      CREATE TABLE IF NOT EXISTS niveau_de_fraicheur (
                        id SERIAL PRIMARY KEY,
                        niveau_de_fraicheur TEXT NOT NULL,
                        active BOOL NOT NULL DEFAULT TRUE
                      )"""

insert_niveau_de_fraicheur = """
                            INSERT INTO niveau_de_fraicheur (niveau_de_fraicheur)
                            VALUES (%s) returning id;
                            """

update_niveau_de_fraicheur = """
                            UPDATE niveau_de_fraicheur 
                            SET niveau_de_fraicheur= %(niveau_de_fraicheur)s
                              active = %(active)s
                            WHERE id = %(id)s returning id;
                            """

change_niveau_de_fraicheur_status = """
                                    UPDATE niveau_de_fraicheur 
                                    SET active = NOT active 
                                    WHERE id =%s; 
                                    """

select_niveau_de_fraicheur_for_diplay = """
                                        SELECT id,niveau_de_fraicheur AS Fraicheur, active, '' AS Change 
                                        FROM niveau_de_fraicheur;
                                        """

select_niveau_de_fraicheur_tous = """
                                  SELECT id,niveau_de_fraicheur 
                                  FROM niveau_de_fraicheur 
                                  WHERE active 
                                  ORDER BY niveau_de_fraicheur ASC;
                                  """

#------------ Tables des liens niveaux de fraicheurs - lieux active -------------#

drop_lien_niveau_de_fraicheur_cooltogo_validated = """
                                                  DROP TABLE IF EXISTS lien_niveau_de_fraicheur_cooltogo_validated;
                                                  """

lien_niveau_de_fraicheur_cooltogo_validated = """
                                              CREATE TABLE IF NOT EXISTS lien_niveau_de_fraicheur_cooltogo_validated (
                                                id SERIAL PRIMARY KEY,
                                                id_cooltogo_validated BIGINT,
                                                id_niveau_de_fraicheur BIGINT
                                              )"""

insert_lien_niveau_de_fraicheur_cooltogo_validated = """
                                                    INSERT INTO lien_niveau_de_fraicheur_cooltogo_validated (id_cooltogo_validated, id_niveau_de_fraicheur)
                                                    VALUES (%(id_cooltogo_validated)s, %(id_niveau_de_fraicheur)s) returning id;
                                                    """

select_lien_niveau_de_fraicheur_cooltogo_validated = """
                                                    SELECT id_niveau_de_fraicheur 
                                                    FROM lien_niveau_de_fraicheur_cooltogo_validated 
                                                    WHERE id_cooltogo_validated=%s; 
                                                    """

update_lien_niveau_de_fraicheur_cooltogo_validated = """
                                                      UPDATE lien_niveau_de_fraicheur_cooltogo_validated 
                                                      SET id_niveau_de_fraicheur= %(id_niveau_de_fraicheur)s
                                                      WHERE id_cooltogo_validated = %(id_cooltogo_validated)s returning id;
                                                      """

delete_lien_niveau_de_fraicheur_cooltogo_validated = """
                                                      DELETE 
                                                      FROM lien_niveau_de_fraicheur_cooltogo_validated 
                                                      WHERE id_cooltogo_validated = %s;
                                                      """

#------- Tables des liens niveaux de fraicheurs - lieux active -------#

drop_projet = """
              DROP TABLE IF EXISTS projet;
              """

projet = """
        CREATE TABLE IF NOT EXISTS projet (
          id SERIAL PRIMARY KEY,
          project_ID TEXT NOT NULL,
          api_key TEXT NOT NULL
        )"""

insert_projet = """
                INSERT INTO projet (project_ID, api_key)
                VALUES (%(project_ID)s, %(api_key)s) 
                returning id;
                """

select_projet_with_id = """
                        SELECT project_ID, api_key 
                        FROM projet 
                        WHERE id=%s; 
                        """

select_projet_information = """
                            SELECT id, project_ID, api_key,'' as Launch, '' as Del 
                            FROM projet; 
                            """

select_selection_projet = """
                          SELECT project_ID, api_key,selection 
                          FROM projet as p 
                          LEFT JOIN selection as s 
                          ON p.id=s.id_projet
                           WHERE s.id=%s; 
                           """

delete_projet_with_id = """
                        DELETE 
                        FROM projet 
                        WHERE id=%s; 
                        """

#------------------------ User profils -------------------------#

# drop_profil = """
#                 DROP TABLE IF EXISTS profils_usager;
#                 """
# profil = """
#           CREATE TABLE IF NOT EXISTS profils_usager (
#             id SERIAL PRIMARY KEY,
#             profils VARCHAR(20)
#           )"""

#---------------------------------------------------------------#
#                          THE END                              #
#---------------------------------------------------------------#
