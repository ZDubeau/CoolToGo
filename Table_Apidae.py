"""----------------------------
Creation date : 2020-06-11
Last update : 2020-07-20
----------------------------"""

import re
import os
import logging
import datetime
import traceback
import sqlalchemy
import pandas as pd
from LoggerModule.FileLogger import FileLogger as FileLogger

from DB_Connexion import DB_connexion
import Table_project as prj
import Table_extraction as extract
import Table_category as ctg
import Table_profil as prf
import Table_relation_eltref_prf as elt_prf
import Table_relation_eltref_ctg as elt_ctg
import Table_relation_category_data_from_apidae as rel_ctg_apidae
import Table_relation_profil_data_from_apidae as rel_prf_apidae
import apidae_extraction as apex  # my function retrieving data from apiade


class data_from_apidaeModel():
    """Classe représentant la table data_from_apidae dans la BDD.

    Raises:
        Exception: Erreur si id_apidae est vide.
        Exception: Erreur si id_selection est vide.
    Returns:
        data_from_apidaeModel: retourne un élément.
    """

    def __init__(self, id_apidae, id_selection, type_apidae, titre, profil_c2g, categorie_c2g, adresse1, adresse2,
                 code_postal, ville, altitude, latitude, longitude, telephone, email, site_web, description_courte,
                 description_detaillee, image, publics, tourisme_adapte, payant, animaux_acceptes, environnement, equipement,
                 services, periode, activites, ouverture, date_debut, date_fin, typologie, bons_plans, dispositions_speciales,
                 service_enfants, service_cyclistes, nouveaute_2020):
        """Initialisation d'un element de selection
        """
        if not id_apidae:
            raise Exception("'id_apidae' should not be empty!")
        if not id_selection:
            raise Exception("'id_selection' should not be empty!")

        self.__id_apidae = id_apidae
        self.__id_selection = id_selection
        self.__type_apidae = type_apidae
        self.__titre = titre
        self.__profil_c2g = profil_c2g
        self.__categorie_c2g = categorie_c2g
        self.__adresse1 = adresse1
        self.__adresse2 = adresse2
        self.__code_postal = code_postal
        self.__ville = ville
        self.__altitude = altitude
        self.__latitude = latitude
        self.__longitude = longitude
        self.__telephone = telephone
        self.__email = email
        self.__site_web = site_web
        self.__description_courte = description_courte
        self.__description_detaillee = description_detaillee
        self.__image = image
        self.__publics = publics
        self.__tourisme_adapte = tourisme_adapte
        self.__payant = payant
        self.__animaux_acceptes = animaux_acceptes
        self.__environnement = environnement
        self.__equipement = equipement
        self.__services = services
        self.__periode = periode
        self.__activites = activites
        self.__ouverture = ouverture
        self.__date_debut = date_debut
        self.__date_fin = date_fin
        self.__typologie = typologie
        self.__bons_plans = bons_plans
        self.__dispositions_speciales = dispositions_speciales
        self.__service_enfants = service_enfants
        self.__service_cyclistes = service_cyclistes
        self.__nouveaute_2020 = nouveaute_2020

    @property
    def id_apidae(self):
        """Retourne la variable __id_apidae.
        """
        return self.__id_apidae

    @property
    def id_selection(self):
        """Retourne la variable __id_selection.
        """
        return self.__id_selection

    @property
    def type_apidae(self):
        """Retourne la variable __type_apidae.
        """
        return self.__type_apidae

    @property
    def titre(self):
        """Retourne la variable __titre.
        """
        return self.__titre

    @property
    def profil_c2g(self):
        """Retourne la variable __profil_c2g.
        """
        return self.__profil_c2g

    @property
    def categorie_c2g(self):
        """Retourne la variable __categorie_c2g.
        """
        return self.__categorie_c2g

    @property
    def adresse1(self):
        """Retourne la variable __adresse1.
        """
        return self.__adresse1

    @property
    def adresse2(self):
        """Retourne la variable __adresse2.
        """
        return self.__adresse2

    @property
    def code_postal(self):
        """Retourne la variable __code_postal.
        """
        return self.__code_postal

    @property
    def ville(self):
        """Retourne la variable __ville.
        """
        return self.__ville

    @property
    def altitude(self):
        """Retourne la variable __altitude.
        """
        return self.__altitude

    @property
    def latitude(self):
        """Retourne la variable __latitude.
        """
        return self.__latitude

    @property
    def longitude(self):
        """Retourne la variable __longitude.
        """
        return self.__longitude

    @property
    def telephone(self):
        """Retourne la variable __telephone.
        """
        return self.__telephone

    @property
    def email(self):
        """Retourne la variable __email.
        """
        return self.__email

    @property
    def site_web(self):
        """Retourne la variable __site_web.
        """
        return self.__site_web

    @property
    def description_courte(self):
        """Retourne la variable __description_courte.
        """
        return self.__description_courte

    @property
    def description_detaillee(self):
        """Retourne la variable __description_detaillee.
        """
        return self.__description_detaillee

    @property
    def image(self):
        """Retourne la variable __image.
        """
        return self.__image

    @property
    def publics(self):
        """Retourne la variable __publics.
        """
        return self.__publics

    @property
    def tourisme_adapte(self):
        """Retourne la variable __tourisme_adapte.
        """
        return self.__tourisme_adapte

    @property
    def payant(self):
        """Retourne la variable __payant.
        """
        return self.__payant

    @property
    def animaux_acceptes(self):
        """Retourne la variable __animaux_acceptes.
        """
        return self.__animaux_acceptes

    @property
    def environnement(self):
        """Retourne la variable __environnement.
        """
        return self.__environnement

    @property
    def equipement(self):
        """Retourne la variable __equipement.
        """
        return self.__equipement

    @property
    def services(self):
        """Retourne la variable __services.
        """
        return self.__services

    @property
    def periode(self):
        """Retourne la variable __periode.
        """
        return self.__periode

    @property
    def activites(self):
        """Retourne la variable __activites.
        """
        return self.__activites

    @property
    def ouverture(self):
        """Retourne la variable __ouverture.
        """
        return self.__ouverture

    @property
    def date_debut(self):
        """Retourne la variable __date_debut.
        """
        return self.__date_debut

    @property
    def date_fin(self):
        """Retourne la variable __date_fin.
        """
        return self.__date_fin

    @property
    def typologie(self):
        """Retourne la variable __typologie.
        """
        return self.__typologie

    @property
    def bons_plans(self):
        """Retourne la variable __bons_plans.
        """
        return self.__bons_plans

    @property
    def dispositions_speciales(self):
        """Retourne la variable __dispositions_speciales.
        """
        return self.__dispositions_speciales

    @property
    def service_enfants(self):
        """Retourne la variable __service_enfants.
        """
        return self.__service_enfants

    @property
    def service_cyclistes(self):
        """Retourne la variable __service_cyclistes.
        """
        return self.__service_cyclistes

    @property
    def nouveaute_2020(self):
        """Retourne la variable __nouveaute_2020.
        """
        return self.__nouveaute_2020


class Data_from_apidae():
    """Classe permettant de gérer les sélections d'un projet"""

    def __init__(self, id_selection=0):
        if not id_selection:
            FileLogger.log(logging.ERROR, "'id_selection' could not be empty!")
            return
        self.__id_selection = id_selection
        self.__connexion = DB_connexion()
        data = self.__connexion.Query_SQL_fetchone(
            prj.select_selection_project, [self.__id_selection])
        self.__project_ID = data[0]
        self.__api_KEY = data[1]
        self.__selection = data[2]
        self.__categories_for_selection_list = []
        data_ctg = self.__connexion.Query_SQL_fetchall(
            ctg.select_category_for_selection_id, [self.__id_selection])
        for line in data_ctg:
            if line[2] is not None:
                self.__categories_for_selection_list.append(line[0])

        self.__element_reference_by_profil_dict = {}
        data_prf = self.__connexion.Query_SQL_fetchall(prf.select_user_profil)
        for profil in data_prf:
            id_profil = profil[0]
            element_reference_list = []
            data_element_reference_by_profil = self.__connexion.Query_SQL_fetchall(
                elt_prf.select_relation_eltref_profil, {'id_profil': id_profil})
            for element_reference in data_element_reference_by_profil:
                element_reference_list.append(element_reference[2])
            self.__element_reference_by_profil_dict[id_profil] = element_reference_list

        self.__element_reference_by_category_dict = {}
        data_prf = self.__connexion.Query_SQL_fetchall(ctg.select_category)
        for category in data_prf:
            id_category = category[0]
            element_reference_list = []
            data_element_reference_by_category = self.__connexion.Query_SQL_fetchall(
                elt_ctg.select_relation_eltref_category, {'id_category': id_category})
            for element_reference in data_element_reference_by_category:
                element_reference_list.append(element_reference[2])
            self.__element_reference_by_category_dict[id_category] = element_reference_list
        # self.__profil_for_selection_list = []
        # data_prf = self.__connexion.Query_SQL_fetchall(
        #     prf.select_profil_for_selection_id, [self.__id_selection])
        # for line in data_prf:
        #     if line[2] is not None:
        #         self.__profil_for_selection_list.append(line[0])

    def __del__(self):
        del self.__connexion
        FileLogger.log(
            logging.DEBUG, "Destruction of data_from_apidae class instance")
        pass

    def __Create(self, data_from_apidae=[]):
        """Insertion des sélections dans la table des data_from_apidaes
        """
        try:
            if not data_from_apidae:
                return
            # Récupération des données dans la bdd
            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_data_from_apidae = sqlalchemy.Table(
                'data_from_apidae',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )
            lines = self.__connexion.engine().connect().execute(
                tInfo_data_from_apidae.insert(None),
                [
                    {
                        'id_apidae': adata_from_apidae.id_apidae,  # mandatory
                        'id_selection': adata_from_apidae.id_selection,  # mandatory
                        'type_apidae': adata_from_apidae.type_apidae,  # needed
                        'titre': adata_from_apidae.titre,  # needed
                        'profil_c2g': adata_from_apidae.profil_c2g,
                        'categorie_c2g': adata_from_apidae.categorie_c2g,
                        'adresse1': adata_from_apidae.adresse1,  # needed
                        'adresse2': adata_from_apidae.adresse2,  # needed
                        'code_postal': adata_from_apidae.code_postal,  # needed
                        'ville': adata_from_apidae.ville,  # needed
                        'altitude': adata_from_apidae.altitude,  # needed
                        'latitude': adata_from_apidae.latitude,  # needed
                        'longitude': adata_from_apidae.longitude,  # needed
                        'telephone': adata_from_apidae.telephone,  # needed
                        'email': adata_from_apidae.email,  # needed
                        'site_web': adata_from_apidae.site_web,  # needed
                        'description_courte': adata_from_apidae.description_courte,  # needed
                        'description_detaillee': adata_from_apidae.description_detaillee,  # needed
                        'image': adata_from_apidae.image,  # needed
                        'publics': adata_from_apidae.publics,
                        'tourisme_adapte': adata_from_apidae.tourisme_adapte,  # needed
                        'payant': adata_from_apidae.payant,  # needed
                        'animaux_acceptes': adata_from_apidae.animaux_acceptes,
                        'environnement': adata_from_apidae.environnement,  # needed
                        'equipement': adata_from_apidae.equipement,
                        'services': adata_from_apidae.services,
                        'periode': adata_from_apidae.periode,
                        'activites': adata_from_apidae.activites,
                        'ouverture': adata_from_apidae.ouverture,  # needed
                        'date_debut': adata_from_apidae.date_debut,  # needed
                        'date_fin': adata_from_apidae.date_fin,  # needed
                        'typologie': adata_from_apidae.typologie,
                        'bons_plans': adata_from_apidae.bons_plans,
                        'dispositions_speciales': adata_from_apidae.dispositions_speciales,
                        'service_enfants': adata_from_apidae.service_enfants,
                        'service_cyclistes': adata_from_apidae.service_cyclistes,
                        'nouveaute_2020': adata_from_apidae.nouveaute_2020,
                    } for adata_from_apidae in data_from_apidae
                ]
            )
            nb_connexion = self.__connexion.number_connections()
            FileLogger.log(
                logging.DEBUG, f"New instance created, number of connexion : {nb_connexion}")
            for adata_from_apidae in data_from_apidae:
                id_data_from_apidae = self.__connexion.Query_SQL_fetchone(select_apidae_with_id_apidae_and_selection, [
                                                                          adata_from_apidae.id_apidae, adata_from_apidae.id_selection])[0]
                if not adata_from_apidae.profil_c2g:
                    list_profil = self.__connexion.Query_SQL_fetchall(
                        prf.select_basic_user_profil)
                    for profil in list_profil:
                        self.__connexion.Insert_SQL(
                            rel_prf_apidae.insert_relation_profil_apidae, [profil[0], id_data_from_apidae])
                else:
                    for profil in adata_from_apidae.profil_c2g:
                        self.__connexion.Insert_SQL(
                            rel_prf_apidae.insert_relation_profil_apidae, [profil, id_data_from_apidae])
                for category in adata_from_apidae.categorie_c2g:
                    self.__connexion.Insert_SQL(
                        rel_ctg_apidae.insert_relation_category_apidae, [category, id_data_from_apidae])
            FileLogger.log(
                logging.DEBUG, f"{lines.rowcount} data_from_apidae(s) for selection: {self.__id_selection} of project_ID: {self.__project_ID} inserted!")
        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Read(self):
        """Lecture des data_from_apidaes pour un projet donné.
        """
        try:

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_data_from_apidae = sqlalchemy.Table(
                'data_from_apidae',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            dico_data_from_apidae = {}

            query = sqlalchemy.select([tInfo_data_from_apidae]).where(sqlalchemy.and_(
                tInfo_data_from_apidae.c.id_selection == self.__id_selection,)
            ).distinct()

            result = self.__connexion.engine().connect().execute(query)
            nb_connexion = self.__connexion.number_connections()
            FileLogger.log(
                logging.DEBUG, f"New instance created, number of connexion : {nb_connexion}")

            if result.rowcount == 0:
                return dico_data_from_apidae
            for row in result:
                adata_from_apidae = data_from_apidaeModel(
                    row[tInfo_data_from_apidae.c.id_apidae],
                    row[tInfo_data_from_apidae.c.id_selection],
                    row[tInfo_data_from_apidae.c.type_apidae],
                    row[tInfo_data_from_apidae.c.titre],
                    row[tInfo_data_from_apidae.c.profil_c2g],
                    row[tInfo_data_from_apidae.c.categorie_c2g],
                    row[tInfo_data_from_apidae.c.adresse1],
                    row[tInfo_data_from_apidae.c.adresse2],
                    row[tInfo_data_from_apidae.c.code_postal],
                    row[tInfo_data_from_apidae.c.ville],
                    row[tInfo_data_from_apidae.c.altitude],
                    row[tInfo_data_from_apidae.c.latitude],
                    row[tInfo_data_from_apidae.c.longitude],
                    row[tInfo_data_from_apidae.c.telephone],
                    row[tInfo_data_from_apidae.c.email],
                    row[tInfo_data_from_apidae.c.site_web],
                    row[tInfo_data_from_apidae.c.description_courte],
                    row[tInfo_data_from_apidae.c.description_detaillee],
                    row[tInfo_data_from_apidae.c.image],
                    row[tInfo_data_from_apidae.c.publics],
                    row[tInfo_data_from_apidae.c.tourisme_adapte],
                    row[tInfo_data_from_apidae.c.payant],
                    row[tInfo_data_from_apidae.c.animaux_acceptes],
                    row[tInfo_data_from_apidae.c.environnement],
                    row[tInfo_data_from_apidae.c.equipement],
                    row[tInfo_data_from_apidae.c.services],
                    row[tInfo_data_from_apidae.c.periode],
                    row[tInfo_data_from_apidae.c.activites],
                    row[tInfo_data_from_apidae.c.ouverture],
                    row[tInfo_data_from_apidae.c.date_debut],
                    row[tInfo_data_from_apidae.c.date_fin],
                    row[tInfo_data_from_apidae.c.typologie],
                    row[tInfo_data_from_apidae.c.bons_plans],
                    row[tInfo_data_from_apidae.c.dispositions_speciales],
                    row[tInfo_data_from_apidae.c.service_enfants],
                    row[tInfo_data_from_apidae.c.service_cyclistes],
                    row[tInfo_data_from_apidae.c.nouveaute_2020]
                )
                key = "{0}_#_{1}".format(
                    adata_from_apidae.id_apidae, adata_from_apidae.id_selection)

                if not key in dico_data_from_apidae:
                    dico_data_from_apidae[key] = adata_from_apidae

            return dico_data_from_apidae

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Update(self, data_from_apidae=[]):
        """Mise à jour des données dans la table data_from_apidae"""

        try:

            if data_from_apidae == None:
                return

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_data_from_apidae = sqlalchemy.Table(
                'data_from_apidae',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            query = tInfo_data_from_apidae.update(None).where(
                sqlalchemy.and_(
                    tInfo_data_from_apidae.c.id_apidae == sqlalchemy.bindparam(
                        'c_id_apidae'),
                    tInfo_data_from_apidae.c.id_selection == int(
                        self.__id_selection),
                )
            ).values(
                type_apidae=sqlalchemy.bindparam('type_apidae'),
                titre=sqlalchemy.bindparam('titre'),
                profil_c2g=sqlalchemy.bindparam('profil_c2g'),
                categorie_c2g=sqlalchemy.bindparam('categorie_c2g'),
                adresse1=sqlalchemy.bindparam('adresse1'),
                adresse2=sqlalchemy.bindparam('adresse2'),
                code_postal=sqlalchemy.bindparam('code_postal'),
                ville=sqlalchemy.bindparam('ville'),
                altitude=sqlalchemy.bindparam('altitude'),
                latitude=sqlalchemy.bindparam('latitude'),
                longitude=sqlalchemy.bindparam('longitude'),
                telephone=sqlalchemy.bindparam('telephone'),
                email=sqlalchemy.bindparam('email'),
                site_web=sqlalchemy.bindparam('site_web'),
                description_courte=sqlalchemy.bindparam(
                    'description_courte'),
                description_detaillee=sqlalchemy.bindparam(
                    'description_detaillee'),
                image=sqlalchemy.bindparam('image'),
                publics=sqlalchemy.bindparam('publics'),
                tourisme_adapte=sqlalchemy.bindparam('tourisme_adapte'),
                payant=sqlalchemy.bindparam('payant'),
                animaux_acceptes=sqlalchemy.bindparam('animaux_acceptes'),
                environnement=sqlalchemy.bindparam('environnement'),
                equipement=sqlalchemy.bindparam('equipement'),
                services=sqlalchemy.bindparam('services'),
                activites=sqlalchemy.bindparam('activites'),
                ouverture=sqlalchemy.bindparam('ouverture'),
                date_debut=sqlalchemy.bindparam('date_debut'),
                date_fin=sqlalchemy.bindparam('date_fin'),
                typologie=sqlalchemy.bindparam('typologie'),
                bons_plans=sqlalchemy.bindparam('bons_plans'),
                dispositions_speciales=sqlalchemy.bindparam(
                    'dispositions_speciales'),
                service_enfants=sqlalchemy.bindparam('service_enfants'),
                service_cyclistes=sqlalchemy.bindparam(
                    'service_cyclistes'),
                nouveaute_2020=sqlalchemy.bindparam('nouveaute_2020'),
            )

            lines = self.__connexion.engine().connect().execute(query,
                                                                [
                                                                    {
                                                                        'c_id_apidae': str(adata_from_apidae.id_apidae),
                                                                        'type_apidae': adata_from_apidae.type_apidae,
                                                                        'titre': adata_from_apidae.titre,
                                                                        'profil_c2g': adata_from_apidae.profil_c2g,
                                                                        'categorie_c2g': adata_from_apidae.categorie_c2g,
                                                                        'adresse1': adata_from_apidae.adresse1,
                                                                        'adresse2': adata_from_apidae.adresse2,
                                                                        'code_postal': adata_from_apidae.code_postal,
                                                                        'ville': adata_from_apidae.ville,
                                                                        'altitude': adata_from_apidae.altitude,
                                                                        'latitude': adata_from_apidae.latitude,
                                                                        'longitude': adata_from_apidae.longitude,
                                                                        'telephone': adata_from_apidae.telephone,
                                                                        'email': adata_from_apidae.email,
                                                                        'site_web': adata_from_apidae.site_web,
                                                                        'description_courte': adata_from_apidae.description_courte,
                                                                        'description_detaillee': adata_from_apidae.description_detaillee,
                                                                        'image': adata_from_apidae.image,
                                                                        'publics': adata_from_apidae.publics,
                                                                        'tourisme_adapte': adata_from_apidae.tourisme_adapte,
                                                                        'payant': adata_from_apidae.payant,
                                                                        'animaux_acceptes': adata_from_apidae.animaux_acceptes,
                                                                        'environnement': adata_from_apidae.environnement,
                                                                        'equipement': adata_from_apidae.equipement,
                                                                        'services': adata_from_apidae.services,
                                                                        'activites': adata_from_apidae.activites,
                                                                        'ouverture': adata_from_apidae.ouverture,
                                                                        'date_debut': adata_from_apidae.date_debut,
                                                                        'date_fin': adata_from_apidae.date_fin,
                                                                        'typologie': adata_from_apidae.typologie,
                                                                        'bons_plans': adata_from_apidae.bons_plans,
                                                                        'dispositions_speciales': adata_from_apidae.dispositions_speciales,
                                                                        'service_enfants': adata_from_apidae.service_enfants,
                                                                        'service_cyclistes': adata_from_apidae.service_cyclistes,
                                                                        'nouveaute_2020': adata_from_apidae.nouveaute_2020,
                                                                    } for adata_from_apidae in data_from_apidae
                                                                ]
                                                                )
            nb_connexion = self.__connexion.number_connections()
            FileLogger.log(
                logging.DEBUG, f"New instance created, number of connexion : {nb_connexion}")
            for adata_from_apidae in data_from_apidae:
                id_data_from_apidae = self.__connexion.Query_SQL_fetchone(select_apidae_with_id_apidae_and_selection, [
                                                                          adata_from_apidae.id_apidae, adata_from_apidae.id_selection])[0]
                self.__connexion.Delete_SQL(
                    rel_prf_apidae.delete_relation_profil_apidae_with_id_data_from_apidae, [id_data_from_apidae])
                self.__connexion.Delete_SQL(
                    rel_ctg_apidae.delete_relation_category_apidae_with_id_data_from_apidae, [id_data_from_apidae])
                if not adata_from_apidae.profil_c2g:
                    list_profil = self.__connexion.Query_SQL_fetchall(
                        prf.select_basic_user_profil)
                    for profil in list_profil:
                        self.__connexion.Insert_SQL(
                            rel_prf_apidae.insert_relation_profil_apidae, [profil[0], id_data_from_apidae])
                else:
                    for profil in adata_from_apidae.profil_c2g:
                        self.__connexion.Insert_SQL(
                            rel_prf_apidae.insert_relation_profil_apidae, [profil, id_data_from_apidae])
                for category in adata_from_apidae.categorie_c2g:
                    self.__connexion.Insert_SQL(
                        rel_ctg_apidae.insert_relation_category_apidae, [category, id_data_from_apidae])
            FileLogger.log(
                logging.DEBUG, f"{lines.rowcount} data_from_apidae(s) for selection: {self.__id_selection} of project_ID: {self.__project_ID} updated!")

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Delete(self, data_from_apidae=[]):
        """Suppression de data_from_apidae(s).
        """
        try:

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_data_from_apidae = sqlalchemy.Table(
                'data_from_apidae',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            lines = 0
            for adata_from_apidae in data_from_apidae:
                id_apidae = re.split(r'_#_', adata_from_apidae)[0]
                query = tInfo_data_from_apidae.delete(None).where(
                    sqlalchemy.and_(
                        tInfo_data_from_apidae.c.id_apidae == id_apidae,
                        tInfo_data_from_apidae.c.id_selection == self.__id_selection
                    )
                )
                line = self.__connexion.engine().connect().execute(query)
                nb_connexion = self.__connexion.number_connections()
                FileLogger.log(
                    logging.DEBUG, f"New instance created, number of connexion : {nb_connexion}")
                lines += int(line.rowcount)
            FileLogger.log(
                logging.DEBUG, f"{lines} data_from_apidae(s) for selection: {self.__id_selection} of project_ID: {self.__project_ID} deleted!")

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def Execute(self):
        """Execution des traitements pour récupérer les data_from_apidae d'un project_ID.
        """

        try:
            # Chargement de toutes les data_from_apidaes pour un project_ID.
            dict_data_from_apidae = self.__Read()
            listUpdate_data_from_apidae = []
            listInsert_data_from_apidae = []
            listOfKeys = []
            data_from_apidae_df = apex.retrive_data_by_selectionId(
                self.__project_ID, self.__api_KEY, self.__selection, self.__id_selection, self.__categories_for_selection_list,  self.__element_reference_by_profil_dict, self.__element_reference_by_category_dict)
            for _i, row in data_from_apidae_df.iterrows():
                adata_from_apidae = data_from_apidaeModel(
                    row['id_apidae'],
                    row['id_selection'],
                    row['type_apidae'],
                    row['titre'],
                    row['profil_c2g'],
                    row['categorie_c2g'],
                    row['adresse1'],
                    row['adresse2'],
                    row['code_postal'],
                    row['ville'],
                    row['altitude'],
                    row['latitude'],
                    row['longitude'],
                    row['telephone'],
                    row['email'],
                    row['site_web'],
                    row['description_courte'],
                    row['description_detaillee'],
                    row['image'],
                    row['publics'],
                    row['tourisme_adapte'],
                    row['payant'],
                    row['animaux_acceptes'],
                    row['environnement'],
                    row['equipement'],
                    row['services'],
                    row['periode'],
                    row['activites'],
                    row['ouverture'],
                    row['date_debut'],
                    row['date_fin'],
                    row['typologie'],
                    row['bons_plans'],
                    row['dispositions_speciales'],
                    row['service_enfants'],
                    row['service_cyclistes'],
                    row['nouveaute_2020']
                )

                currentKey = "{0}_#_{1}".format(
                    adata_from_apidae.id_apidae, adata_from_apidae.id_selection)

                if currentKey in listOfKeys:  # Si on a déjà traité cette clé.
                    continue
                listOfKeys.append(currentKey)
                if not currentKey in dict_data_from_apidae:
                    listInsert_data_from_apidae.append(adata_from_apidae)
                else:
                    listUpdate_data_from_apidae.append(adata_from_apidae)
                    del dict_data_from_apidae[currentKey]

            # Update
            if listUpdate_data_from_apidae:
                FileLogger.log(
                    logging.DEBUG, f"data_from_apidae list for selection: {self.__id_selection} of project_ID: {self.__project_ID} Update in progress...")
                self.__Update(listUpdate_data_from_apidae)

            # Delete
            if dict_data_from_apidae:
                FileLogger.log(
                    logging.DEBUG, f"data_from_apidae list for selection: {self.__id_selection} of project_ID: {self.__project_ID} Delete in progress...")
                self.__Delete(dict_data_from_apidae)

            # insert
            if listInsert_data_from_apidae:
                FileLogger.log(
                    logging.DEBUG, f"data_from_apidae list for selection: {self.__id_selection} of project_ID: {self.__project_ID} Insert in progress...")
                self.__Create(listInsert_data_from_apidae)

            # update of extract data
            self.__connexion.Insert_SQL(extract.insert_selection_extraction, [
                                        self.__id_selection, int(len(data_from_apidae_df.index))])

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())


drop_apidae = """
                DROP TABLE IF EXISTS data_from_apidae CASCADE;
                """

apidae = """
        CREATE TABLE IF NOT EXISTS data_from_apidae (
            id_data_from_apidae SERIAL PRIMARY KEY,
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

insert_apidae = """
                INSERT INTO data_from_apidae (
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
                returning id_data_from_apidae;
                """

select_apidae_display = """
                        SELECT MIN(dfa.id_data_from_apidae) AS id, dfa.id_apidae AS id_apidae,
                                array_to_string(array_agg(DISTINCT dfa.id_selection), ', ', '*') AS id_selection, 
                                dfa.type_apidae AS type_apidae, dfa.titre AS titre,
                                CASE 
                                    WHEN pae.id_data_from_apidae IS NULL THEN array_to_string(array_agg(DISTINCT p.profil), ', ', '*')
                                    ELSE array_to_string(array_agg(DISTINCT pe.profil), ', ', '*')
                                    END AS profil_c2g,
                                CASE
                                    WHEN cae.id_data_from_apidae IS NULL THEN array_to_string(array_agg(DISTINCT c.category_name), ', ', '*')
                                    ELSE array_to_string(array_agg(DISTINCT ce.category_name), ', ', '*')
                                    END AS categorie_c2g,
                                dfa.adresse1 AS adresse1, dfa.adresse2 AS adresse2, dfa.code_postal AS code_postal, 
                                dfa.ville AS ville, dfa.altitude AS altitude, dfa.longitude AS longitude,
                                dfa.latitude AS latitude, dfa.telephone AS telephone, dfa.email AS email, 
                                dfa.site_web AS site_web, dfa.description_courte AS description_courte, 
                                dfa.description_detaillee AS description_detaillee,
                                dfa.image AS image, dfa.publics AS publics, dfa.tourisme_adapte AS tourisme_adapte, 
                                dfa.payant AS payant, dfa.animaux_acceptes AS animaux_acceptes, dfa.environnement AS environnement, 
                                dfa.equipement AS equipement, dfa.services AS services, dfa.periode AS periode, dfa.activites AS activites, 
                                dfa.ouverture AS ouverture, dfa.date_debut AS date_debut, dfa.date_fin AS date_fin, dfa.typologie AS typologie, 
                                dfa.bons_plans AS bons_plans, dfa.dispositions_speciales AS disposition_speciales, dfa.service_enfants AS services_enfants, 
                                dfa.service_cyclistes AS service_cyclistes, dfa.nouveaute_2020 AS nouveaute_2020, '' AS modifier
                            FROM data_from_apidae AS dfa
                            LEFT JOIN category_apidae AS ca ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                            LEFT JOIN category AS c ON ca.id_category = c.id_category
                            LEFT JOIN category_apidae_edited AS cae ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                            LEFT JOIN category AS ce ON cae.id_category = ce.id_category
                            LEFT JOIN profil_apidae AS pa ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                            LEFT JOIN profil AS p ON pa.id_profil = p.id_profil
                            LEFT JOIN profil_apidae_edited AS pae ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                            LEFT JOIN profil AS pe ON pae.id_profil = pe.id_profil
                            GROUP BY dfa.id_apidae, dfa.type_apidae, dfa.titre,pae.id_data_from_apidae, cae.id_data_from_apidae,
                                dfa.adresse1, dfa.adresse2, dfa.code_postal, dfa.ville,dfa.altitude, dfa.longitude, 
                                dfa.latitude, dfa.telephone, dfa.email, dfa.site_web, dfa.description_courte,
                                dfa.description_detaillee, dfa.image, dfa.publics, dfa.tourisme_adapte, dfa.payant, 
                                dfa.animaux_acceptes, dfa.environnement, dfa.equipement, dfa.services, dfa.periode, 
                                dfa.activites, dfa.ouverture, dfa.date_debut, dfa.date_fin, dfa.typologie, 
                                dfa.bons_plans, dfa.dispositions_speciales, dfa.service_enfants, dfa.service_cyclistes, dfa.nouveaute_2020;
                        """

select_apidae_category_display = """
                                SELECT a.*, sc.id_category AS id_catégorie, 
                                    array_to_string(array_agg(c.category_name), ', ', '*') AS catégorie_ctg, '' AS modifir
                                FROM data_from_apidae AS a
                                LEFT JOIN selection_category AS sc
                                ON a.id_selection = sc.id_selection
                                LEFT JOIN category AS c
                                ON sc.id_category=c.id_category
                                GROUP BY a.id_data_from_apidae, a.*, sc.id_category
                                ORDER BY id_data_from_apidae ASC;
                                """

select_apidae = """
                SELECT *
                FROM data_from_apidae
                ORDER BY id_data_from_apidae ASC;
                """

select_apidae_selection_display = """
                                    SELECT selection.description AS selection, data_from_apidae.*, '' as Modifier
                                    FROM selection
                                    RIGHT JOIN data_from_apidae
                                    ON selection.id_selection = data_from_apidae.id_selection
                                    ORDER BY id_data_from_apidae ASC;
                                """

select_apidae_1_id = """
                    SELECT dfa.id_apidae AS id_apidae, dfa.type_apidae AS type_apidae, dfa.titre AS titre,
                                array_to_json(array_agg(DISTINCT pa.id_profil)) AS profil_c2g, 
                                array_to_json(array_agg(DISTINCT ca.id_category)) AS categorie_c2g, 
                                dfa.adresse1 AS adresse1, dfa.adresse2 AS adresse2, dfa.code_postal AS code_postal, 
                                dfa.ville AS ville, dfa.altitude AS altitude, dfa.longitude AS longitude, 
                                dfa.latitude AS latitude, dfa.telephone AS telephone, dfa.email AS email, 
                                dfa.site_web AS site_web, dfa.description_courte AS description_courte,
                                dfa.description_detaillee AS description_detaillee, dfa.image AS image, 
                                dfa.publics AS publics, dfa.tourisme_adapte AS tourisme_adapte, 
                                dfa.payant AS payant, dfa.environnement AS environnement, dfa.ouverture AS ouverture,
                                dfa.date_debut AS date_debut, dfa.date_fin AS date_fin
                    FROM data_from_apidae AS dfa
                    LEFT JOIN category_apidae AS ca 
                    ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                    LEFT JOIN profil_apidae AS pa
                    ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                    WHERE dfa.id_data_from_apidae = %s
                    GROUP BY dfa.id_apidae, dfa.type_apidae, dfa.titre, dfa.adresse1, dfa.adresse2, dfa.code_postal, 
                                dfa.ville,dfa.altitude, dfa.longitude, dfa.latitude, dfa.telephone, dfa.email, 
                                dfa.site_web, dfa.description_courte, dfa.description_detaillee,
                                dfa.image, dfa.publics, dfa.tourisme_adapte, dfa.payant, dfa.environnement, 
                                dfa.ouverture, dfa.date_debut, dfa.date_fin
                    LIMIT 1;
                    """

select_apidae_with_id_apidae_and_selection = """
                                            SELECT id_data_from_apidae
                                            FROM data_from_apidae
                                            WHERE id_apidae = %s and id_selection =%s;
                                            """

select_apidae_with_categorie_list_and_profil_list = """
                                                    SELECT DISTINCT(dfa.id_apidae) AS id_apidae, 
                                                        MIN(dfa.id_data_from_apidae) AS id_data_from_apidae
                                                    FROM data_from_apidae as dfa
                                                    LEFT JOIN category_apidae AS ca 
                                                    ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                                                    LEFT JOIN profil_apidae AS pa
                                                    ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                                                    LEFT JOIN category_apidae_edited AS cae 
                                                    ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                                                    LEFT JOIN profil_apidae_edited AS pae
                                                    ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                                                    WHERE pa.id_profil IN %s AND ca.id_category IN %s AND (
                                                        dfa.longitude<>'NaN' AND dfa.latitude<>'NaN') AND 
                                                    cae.id IS NULL AND pae.id IS NULL
                                                    GROUP BY dfa.id_apidae;
                                                    """

select_apidae_with_categorie_list_edited_and_profil_list_edited = """
                                                    SELECT DISTINCT(dfa.id_apidae) AS id_apidae, 
                                                        MIN(dfa.id_data_from_apidae) AS id_data_from_apidae
                                                    FROM data_from_apidae as dfa
                                                    LEFT JOIN category_apidae_edited AS cae 
                                                    ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                                                    LEFT JOIN profil_apidae_edited AS pae
                                                    ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                                                    WHERE pae.id_profil IN %s AND cae.id_category IN %s AND (
                                                        dfa.longitude<>'NaN' AND dfa.latitude<>'NaN')
                                                    GROUP BY dfa.id_apidae;
                                                    """

select_apidae_with_categorie_list_edited_and_profil_list = """
                                                    SELECT DISTINCT(dfa.id_apidae) AS id_apidae, 
                                                        MIN(dfa.id_data_from_apidae) AS id_data_from_apidae
                                                    FROM data_from_apidae as dfa
                                                    LEFT JOIN profil_apidae AS pa
                                                    ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                                                    LEFT JOIN category_apidae_edited AS cae 
                                                    ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                                                    LEFT JOIN profil_apidae_edited AS pae
                                                    ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                                                    WHERE pa.id_profil IN %s AND cae.id_category IN %s AND (
                                                        dfa.longitude<>'NaN' AND dfa.latitude<>'NaN') AND 
                                                        pae.id IS NULL 
                                                    GROUP BY dfa.id_apidae;
                                                    """

select_apidae_with_categorie_list_and_profil_list_edited = """
                                                    SELECT DISTINCT(dfa.id_apidae) AS id_apidae, 
                                                        MIN(dfa.id_data_from_apidae) AS id_data_from_apidae
                                                    FROM data_from_apidae as dfa
                                                    LEFT JOIN category_apidae AS ca 
                                                    ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                                                    LEFT JOIN category_apidae_edited AS cae 
                                                    ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                                                    LEFT JOIN profil_apidae_edited AS pae
                                                    ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                                                    WHERE pae.id_profil IN %s AND ca.id_category IN %s AND (
                                                        dfa.longitude<>'NaN' AND dfa.latitude<>'NaN') AND 
                                                        cae.id IS NULL 
                                                    GROUP BY dfa.id_apidae;
                                                    """

select_apidae_1_id_apidae = """
                            SELECT dfa.id_apidae AS id_apidae, dfa.type_apidae AS type_apidae, dfa.titre AS titre,
                                array_to_json(array_agg(DISTINCT pa.id_profil)) AS profil_c2g, 
                                array_to_json(array_agg(DISTINCT ca.id_category)) AS categorie_c2g, 
                                dfa.adresse1 AS adresse1, dfa.adresse2 AS adresse2, dfa.code_postal AS code_postal, 
                                dfa.ville AS ville, dfa.altitude AS altitude,
                                dfa.longitude AS longitude, dfa.latitude AS latitude, dfa.telephone AS telephone, 
                                dfa.email AS email, dfa.site_web AS site_web, dfa.description_courte AS description_courte, 
                                dfa.description_detaillee AS description_detaillee,
                                dfa.image AS image, dfa.publics AS publics, dfa.tourisme_adapte AS tourisme_adapte, 
                                dfa.payant AS payant, dfa.environnement AS environnement, dfa.ouverture AS ouverture,
                                dfa.date_debut AS date_debut, dfa.date_fin AS date_fin
                            FROM data_from_apidae AS dfa
                            LEFT JOIN category_apidae AS ca 
                            ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                            LEFT JOIN profil_apidae AS pa
                            ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                            WHERE dfa.id_apidae = %s
                            GROUP BY dfa.id_apidae, dfa.type_apidae, dfa.titre, dfa.adresse1, dfa.adresse2, dfa.code_postal, 
                                dfa.ville,dfa.altitude, dfa.longitude, dfa.latitude, dfa.telephone, dfa.email, dfa.site_web, 
                                dfa.description_courte, dfa.description_detaillee, dfa.image, dfa.publics, dfa.tourisme_adapte,
                                dfa.payant, dfa.environnement, dfa.ouverture, dfa.date_debut, dfa.date_fin
                            LIMIT 1;
                            """

select_apidae_all_data = """
                            SELECT MIN(dfa.id_data_from_apidae) AS id, dfa.id_apidae AS id_apidae, dfa.type_apidae AS type_apidae, dfa.titre AS titre,
                                array_to_string(array_agg(DISTINCT p.profil), ', ', '*') AS profil_c2g, 
                                array_to_string(array_agg(DISTINCT c.category_name), ', ', '*') AS categorie_c2g, 
                                dfa.adresse1 AS adresse1, dfa.adresse2 AS adresse2, dfa.code_postal AS code_postal, 
                                dfa.ville AS ville, dfa.altitude AS altitude, dfa.longitude AS longitude,
                                dfa.latitude AS latitude, dfa.telephone AS telephone, dfa.email AS email, 
                                dfa.site_web AS site_web, dfa.description_courte AS description_courte, 
                                dfa.description_detaillee AS description_detaillee,
                                dfa.image AS image, dfa.publics AS publics, dfa.tourisme_adapte AS tourisme_adapte, 
                                dfa.payant AS payant, dfa.environnement AS environnement, dfa.ouverture AS ouverture,
                                dfa.date_debut AS date_debut, dfa.date_fin AS date_fin, '' AS modifier
                            FROM data_from_apidae AS dfa
                            LEFT JOIN category_apidae AS ca ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                            LEFT JOIN category AS c ON ca.id_category = c.id_category
                            LEFT JOIN profil_apidae AS pa ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                            LEFT JOIN profil AS p ON pa.id_profil = p.id_profil
                            GROUP BY dfa.id_apidae, dfa.type_apidae, dfa.titre, dfa.adresse1, 
                                dfa.adresse2, dfa.code_postal, dfa.ville,dfa.altitude, dfa.longitude, 
                                dfa.latitude, dfa.telephone, dfa.email, dfa.site_web, dfa.description_courte,
                                dfa.description_detaillee, dfa.image, dfa.publics, dfa.tourisme_adapte, dfa.payant, 
                                dfa.environnement, dfa.ouverture, dfa.date_debut, dfa.date_fin;
                            """

select_apidae_all_data_with_data_edited = """
                            SELECT MIN(dfa.id_data_from_apidae) AS id, dfa.id_apidae AS id_apidae, 
                                dfa.type_apidae AS type_apidae, dfa.titre AS titre,
                            CASE 
                                WHEN pae.id_data_from_apidae IS NULL THEN array_to_string(array_agg(DISTINCT p.profil), ', ', '*')
                                ELSE array_to_string(array_agg(DISTINCT pe.profil), ', ', '*')
                                END AS profil_c2g,
                            CASE
                                WHEN cae.id_data_from_apidae IS NULL THEN array_to_string(array_agg(DISTINCT c.category_name), ', ', '*')
                                ELSE array_to_string(array_agg(DISTINCT ce.category_name), ', ', '*')
                                END AS categorie_c2g, 
                                dfa.adresse1 AS adresse1, dfa.adresse2 AS adresse2, dfa.code_postal AS code_postal, 
                                dfa.ville AS ville, dfa.altitude AS altitude, dfa.longitude AS longitude,
                                dfa.latitude AS latitude, dfa.telephone AS telephone, dfa.email AS email, 
                                dfa.site_web AS site_web, dfa.description_courte AS description_courte, 
                                dfa.description_detaillee AS description_detaillee,
                                dfa.image AS image, dfa.publics AS publics, dfa.tourisme_adapte AS tourisme_adapte, 
                                dfa.payant AS payant, dfa.environnement AS environnement, dfa.ouverture AS ouverture,
                                dfa.date_debut AS date_debut, dfa.date_fin AS date_fin, '' AS modifier
                            FROM data_from_apidae AS dfa
                            LEFT JOIN category_apidae AS ca ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                            LEFT JOIN category AS c ON ca.id_category = c.id_category
                            LEFT JOIN category_apidae_edited AS cae ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                            LEFT JOIN category AS ce ON cae.id_category = ce.id_category
                            LEFT JOIN profil_apidae AS pa ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                            LEFT JOIN profil AS p ON pa.id_profil = p.id_profil
                            LEFT JOIN profil_apidae_edited AS pae ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                            LEFT JOIN profil AS pe ON pae.id_profil = pe.id_profil
                            GROUP BY dfa.id_apidae, dfa.type_apidae, dfa.titre,
                                pae.id_data_from_apidae, cae.id_data_from_apidae,
                                dfa.adresse1, dfa.adresse2, dfa.code_postal, dfa.ville,dfa.altitude, dfa.longitude,
                                dfa.latitude, dfa.telephone, dfa.email, dfa.site_web, dfa.description_courte,
                                dfa.description_detaillee, dfa.image, dfa.publics, dfa.tourisme_adapte, dfa.payant, 
                                dfa.environnement, dfa.ouverture, dfa.date_debut, dfa.date_fin;
                            """

select_apidae_1_id_with_data_edited = """
                            SELECT MIN(dfa.id_data_from_apidae) AS id, dfa.id_apidae AS id_apidae, 
                                dfa.type_apidae AS type_apidae, dfa.titre AS titre,
                            CASE 
                                WHEN pae.id_data_from_apidae IS NULL THEN array_agg(DISTINCT p.id_profil)
                                ELSE array_agg(DISTINCT pe.id_profil)
                                END AS profil_c2g,
                            CASE
                                WHEN cae.id_data_from_apidae IS NULL THEN array_agg(DISTINCT c.id_category)
                                ELSE array_agg(DISTINCT ce.id_category)
                                END AS categorie_c2g, 
                                dfa.adresse1 AS adresse1, dfa.adresse2 AS adresse2, dfa.code_postal AS code_postal, 
                                dfa.ville AS ville, dfa.altitude AS altitude, dfa.longitude AS longitude,
                                dfa.latitude AS latitude, dfa.telephone AS telephone, dfa.email AS email, 
                                dfa.site_web AS site_web, dfa.description_courte AS description_courte, 
                                dfa.description_detaillee AS description_detaillee,
                                dfa.image AS image, dfa.publics AS publics, dfa.tourisme_adapte AS tourisme_adapte, 
                                dfa.payant AS payant, dfa.environnement AS environnement, dfa.ouverture AS ouverture,
                                dfa.date_debut AS date_debut, dfa.date_fin AS date_fin, '' AS modifier
                            FROM data_from_apidae AS dfa
                            LEFT JOIN category_apidae AS ca ON dfa.id_data_from_apidae = ca.id_data_from_apidae
                            LEFT JOIN category AS c ON ca.id_category = c.id_category
                            LEFT JOIN category_apidae_edited AS cae ON dfa.id_data_from_apidae = cae.id_data_from_apidae
                            LEFT JOIN category AS ce ON cae.id_category = ce.id_category
                            LEFT JOIN profil_apidae AS pa ON dfa.id_data_from_apidae = pa.id_data_from_apidae
                            LEFT JOIN profil AS p ON pa.id_profil = p.id_profil
                            LEFT JOIN profil_apidae_edited AS pae ON dfa.id_data_from_apidae = pae.id_data_from_apidae
                            LEFT JOIN profil AS pe ON pae.id_profil = pe.id_profil
                            WHERE dfa.id_data_from_apidae = %s
                            GROUP BY dfa.id_apidae, dfa.type_apidae, dfa.titre,
                                pae.id_data_from_apidae, cae.id_data_from_apidae,
                                dfa.adresse1, dfa.adresse2, dfa.code_postal, dfa.ville,dfa.altitude, dfa.longitude,
                                dfa.latitude, dfa.telephone, dfa.email, dfa.site_web, dfa.description_courte,
                                dfa.description_detaillee, dfa.image, dfa.publics, dfa.tourisme_adapte, dfa.payant, 
                                dfa.environnement, dfa.ouverture, dfa.date_debut, dfa.date_fin;
                            """

select_apidae_edit = """
                    SELECT MIN(apidae.id_data_from_apidae) AS id, apidae.id_apidae AS id_apidae, apidae.titre AS titre,
                        CASE 
                            WHEN pae.id_data_from_apidae IS NULL THEN array_to_string(array_agg(DISTINCT p.profil), ', ', '*')
                            ELSE array_to_string(array_agg(DISTINCT pe.profil), ', ', '*')
                            END AS profil_c2g,
                        CASE
                            WHEN cae.id_data_from_apidae IS NULL THEN array_to_string(array_agg(DISTINCT c.category_name), ', ', '*')
                            ELSE array_to_string(array_agg(DISTINCT ce.category_name), ', ', '*')
                            END AS categorie_c2g
                    FROM data_from_apidae AS apidae
                    LEFT JOIN category_apidae AS ca ON apidae.id_data_from_apidae = ca.id_data_from_apidae
                    LEFT JOIN category AS c ON ca.id_category = c.id_category
                    LEFT JOIN category_apidae_edited AS cae ON apidae.id_data_from_apidae = cae.id_data_from_apidae
                    LEFT JOIN category AS ce ON ca.id_category = ce.id_category
                    LEFT JOIN profil_apidae AS pa ON apidae.id_data_from_apidae = pa.id_data_from_apidae
                    LEFT JOIN profil AS p ON pa.id_profil = p.id_profil
                    LEFT JOIN profil_apidae_edited AS pae ON apidae.id_data_from_apidae = pae.id_data_from_apidae
                    LEFT JOIN profil AS pe ON pae.id_profil = pe.id_profil
                    WHERE apidae.id_data_from_apidae=%s
                    GROUP BY apidae.id_apidae, apidae.titre,pae.id_data_from_apidae,cae.id_data_from_apidae;
                    """

delete_apidae_project_id = """
                            DELETE
                            FROM data_from_apidae
                            WHERE id_selection IN (
                                SELECT id_data_from_apidae
                                FROM selection
                                WHERE id_project=%s);
                            """
