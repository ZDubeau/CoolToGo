"""----------------------------
Creation date : 2020-06-11
Last update : 2020-07-07
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


class elementreferenceModel():
    """Classe représentant la table elementreference dans la BDD.

    Raises:
        Exception: Erreur si id_elref_in_apidae est vide.
        Exception: Erreur si description est vide.
    Returns:
        elementreferenceModel: retourne un élément.
    """

    def __init__(self, id_elref_in_apidae, description):
        """Initialisation d'un elementreference
        """
        if not id_elref_in_apidae:
            raise Exception("'id_elref_in_apidae' should not be empty!")
        if not description:
            raise Exception("'description' should not be empty!")
        self.__id_elref_in_apidae = id_elref_in_apidae
        self.__description = description

    @property
    def id_elref_in_apidae(self):
        """Retourne la variable __id_elref_in_apidae.
        """
        return self.__id_elref_in_apidae

    @property
    def description(self):
        """Retourne la variable __description.
        """
        return self.__description


class elementReference():
    """Classe permettant de gérer les elements de référence
    """

    def __init__(self, filename=None, dataframe=pd.DataFrame({'P': []})):
        if not filename:
            if dataframe.empty:
                FileLogger.log(
                    logging.ERROR, "'filename' and 'dataframe' can not both be empty!")
                return
            else:
                self.__df = dataframe
        else:
            extension = str.split(filename, '.')[1]
            if extension == 'xls':
                self.__df = pd.read_excel(filename)
            else:
                FileLogger.log(logging.ERROR, "Extension must be xls !")
                return
        self.__connexion = DB_connexion()
        self.__instance = self.__connexion.engine().connect()

    def __Create(self, element_reference=[]):
        """Insertion des sélections dans la table des elementreference
        """
        try:
            if not element_reference:
                return
            # Récupération des données dans la bdd
            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_elementreference = sqlalchemy.Table(
                'elementreference',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )
            with self.__instance.connect():
                lines = self.__instance.execute(
                    tInfo_elementreference.insert(None),
                    [
                        {
                            'id_elref_in_apidae': aelement_reference.id_elref_in_apidae,
                            'description': aelement_reference.description,
                        } for aelement_reference in element_reference
                    ]
                )

            FileLogger.log(
                logging.DEBUG, f"{lines.rowcount} elementreference(s) inserted!")
        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Read(self):
        """Lecture des elementreferences pour un projet donné.
        """
        try:

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_elementreference = sqlalchemy.Table(
                'elementreference',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            dico_elementreference = {}
            with self.__instance.connect():

                query = sqlalchemy.select([tInfo_elementreference]).distinct()

                result = self.__instance.execute(query)

                if result.rowcount == 0:
                    return dico_elementreference
                for row in result:
                    aelement_reference = elementreferenceModel(
                        row[tInfo_elementreference.c.id_elref_in_apidae],
                        row[tInfo_elementreference.c.description],
                    )
                    key = "{0}".format(
                        aelement_reference.id_elref_in_apidae)

                    if not key in dico_elementreference:
                        dico_elementreference[key] = aelement_reference

            return dico_elementreference

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Update(self, element_reference=[]):
        """Mise à jour des données dans la table elementreference
        """
        try:

            if element_reference == None:
                return

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_elementreference = sqlalchemy.Table(
                'elementreference',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            with self.__instance.connect():

                query = tInfo_elementreference.update(None).where(
                    tInfo_elementreference.c.id_elref_in_apidae == sqlalchemy.bindparam(
                        'c_id_elref_in_apidae'),
                ).values(
                    description=sqlalchemy.bindparam('description'),
                )

                lines = self.__instance.execute(query,
                                                [
                                                    {
                                                        'c_id_elref_in_apidae': aelement_reference.id_elref_in_apidae,
                                                        'description': aelement_reference.description,
                                                    } for aelement_reference in element_reference
                                                ]
                                                )
            FileLogger.log(
                logging.DEBUG, f"{lines.rowcount} elementreference(s)mù updated!")

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Delete(self, element_reference=[]):
        """Suppression de elementreference(s).
        """
        try:

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_elementreference = sqlalchemy.Table(
                'elementreference',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            with self.__instance.connect():
                lines = 0
                for aelement_reference in element_reference:
                    query = tInfo_elementreference.delete(None).where(
                        tInfo_elementreference.c.id_elref_in_apidae == aelement_reference,
                    )
                    line = self.__instance.execute(query)
                    lines += int(line.rowcount)
            FileLogger.log(
                logging.DEBUG, f"{lines} elementreference(s) deleted!")

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def Execute(self):
        """Execution des traitements pour récupérer les elementreference.
        """

        try:
            # Chargement de toutes les elementreferences pour un project_ID.
            dict_elementreference = self.__Read()
            listUpdate_elementreference = []
            listInsert_elementreference = []
            listOfKeys = []

            for _i, row in self.__df.iterrows():
                aelement_reference = elementreferenceModel(
                    row['Identifiant'],
                    row['Libellé français']
                )
                currentKey = "{0}".format(
                    aelement_reference.id_elref_in_apidae)

                if currentKey in listOfKeys:  # Si on a déjà traité cette clé.
                    continue
                listOfKeys.append(currentKey)
                if not currentKey in dict_elementreference:
                    listInsert_elementreference.append(aelement_reference)
                else:
                    listUpdate_elementreference.append(aelement_reference)
                    del dict_elementreference[currentKey]

            # Update
            if listUpdate_elementreference:
                FileLogger.log(
                    logging.DEBUG, f"elementreference Update in progress...")
                self.__Update(listUpdate_elementreference)

            # Delete
            if dict_elementreference:
                FileLogger.log(
                    logging.DEBUG, f"elementreference Delete in progress...")
                self.__Delete(dict_elementreference)

            # insert
            if listInsert_elementreference:
                FileLogger.log(
                    logging.DEBUG, f"elementreference Insert in progress...")
                self.__Create(listInsert_elementreference)

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def Close(self):
        self.__connexion.close()
        self.__instance.close()

    @property
    def df(self):
        return self.__df


drop_elementRef = """
                    DROP TABLE IF EXISTS elementreference CASCADE;
                    """

elementRef = """
             CREATE TABLE IF NOT EXISTS elementreference (
                id_eltref SERIAL PRIMARY KEY,
                id_elref_in_apidae BIGINT,
                description TEXT
            )"""

select_elementRef = """
                            SELECT *
                            FROM elementreference; 
                            """

insert_elementRef = """
                    INSERT INTO elementreference (
                        id_elref_in_apidae, description)
                    VALUES (
                        %(id_eltref_in_apidae)s, %(description)s)
                        returning id_eltRef;
                    """

select_elementRef_with_id = """
                            SELECT *
                            FROM elementreference 
                            WHERE id_eltref=%s; 
                            """

select_elementRef_with_id_in_apidae = """
                            SELECT er.id_eltref
                            FROM elementreference AS er
                            WHERE er.id_elref_in_apidae=%s; 
                            """

delete_elementRef = """
                    DELETE 
                    FROM elementreference 
                    WHERE id_eltref=%s; 
                    """

delete_elementRef_not_used = """
                    DELETE 
                    FROM elementreference 
                    WHERE id_eltref IN (SELECT DISTINCT(er.id_eltref) 
                                            FROM elementreference AS er 
                                                LEFT JOIN eltref_category AS ec ON er.id_eltref=ec.id_eltref 
                                                LEFT JOIN eltref_profil AS ep ON er.id_eltref=ep.id_eltref 
                                            WHERE ep.id_eltref IS NULL AND ec.id_eltref IS NULL); 
                    """
