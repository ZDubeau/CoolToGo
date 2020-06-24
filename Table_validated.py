drop_cooltogo_validated = """
                            DROP TABLE IF EXISTS cooltogo_validated;
                            """

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
                            VALUES (%(id_apidae)s, %(Lieu_event)s, %(X)s, %(Y)s, %(name)s, %(Adresse1)s, %(Adresse2)s, %(Code_postal)s, %(Ville)s, %(telephone)s, %(email)s, %(site_web)s, %(Description_Teaser)s, %(Description)s,%(Images)s, %(Publics)s, %(styleUrl)s, %(styleHash)s, %(Type)s, %(Catégories)s, %(Accessibilité)s, %(payant)s, %(Plus_d_infos_et_horaires)s, %(Dates_début)s, %(Dates_fin)s) 
                            returning id;
                            """

select_id_cooltogo_validated = """
                                SELECT id AS id_valide 
                                FROM cooltogo_validated 
                                WHERE id_apidae = %s; 
                                """

select_cooltogo_validated = """
                            SELECT * 
                            FROM cooltogo_validated; 
                            """

select_cooltogo_validated_for_display = """
                                        SELECT *, '' as Edit, '' as Del 
                                        FROM cooltogo_validated 
                                        ORDER BY id ASC; 
                                        """

select_cooltogo_validate_with_id = """
                                    SELECT * 
                                    FROM cooltogo_validated 
                                    WHERE id=%s; 
                                    """

select_max_id_from_cooltogo_validated = """
                                        SELECT MAX(id) 
                                        FROM cooltogo_validated; 
                                        """

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
                                Type =%(Type)s, 
                                Catégories = %(Catégories)s, 
                                Accessibilité = %(Accessibilité)s, 
                                payant = %(payant)s, 
                                Plus_d_infos_et_horaires = %(Plus_d_infos_et_horaires)s, 
                                Dates_début = %(Dates_début)s, 
                                Dates_fin =%(Dates_fin)s
                            WHERE id_apidae = %(id_apidae)s 
                            returning id;
                            """

delete_from_cooltogo_validated_with_id = """
                                        DELETE 
                                        FROM cooltogo_validated 
                                        WHERE id=%s; 
                                        """
