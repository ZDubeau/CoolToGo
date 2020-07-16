""" 
Project CoolToGo
----------------------------
Creation date : 2020-06-11
Last update : 2020-07-01
----------------------------
"""

import pandas as pd
import logging
from LoggerModule.FileLogger import FileLogger as FileLogger
from DB_Connexion import DB_connexion
import os
import sqlalchemy
import datetime
import traceback
import re

import Table_project as prj
import apidae_extraction as apex  # my function retrieving data from apiade


class selectionModel():
    """Classe représentant la table selection dans la BDD.

    Raises:
        Exception: Erreur si id_project est vide.
        Exception: Erreur si la selection est vide.
        Exception: Erreur si la description est vide.

    Returns:
        selectionModel: retourne un élément.
    """

    def __init__(self, id_project, selection, description):
        """Initialisation d'un element de selection
        """
        if not id_project:
            raise Exception("'id_project' should not be empty!")
        if not selection:
            raise Exception("'selection' should not be empty!")
        if not description:
            raise Exception("'description' should not be empty!")

        self.__id_project = id_project
        self.__selection = selection
        self.__description = description

    def __str__(self):
        """Représentation sous forme de string d'une selection.
        """
        return "id_project: {0} -- selection : {1} -- description : {2}"\
            .format(self.__id_project, self.__selection, self.__description)

    @property
    def id_project(self):
        """Retourne la variable __id_project.
        """
        return self.__id_project

    @property
    def selection(self):
        """Retourne la variable __selection.
        """
        return self.__selection

    @property
    def description(self):
        """Retourne la variable __description.
        """
        return self.__description


class Selection():
    """Classe permettant de gérer les sélections d'un projet
    """

    def __init__(self, id_project=0):
        if not id_project:
            FileLogger.log(logging.ERROR, "'id_project' could not be empty!")
            return
        self.__id_project = id_project
        self.__connexion = DB_connexion()
        self.__instance = self.__connexion.instance()
        data = self.__connexion.Query_SQL_fetchone(
            prj.select_project_with_id, [self.__id_project])
        self.__project_ID = data[0]
        self.__api_KEY = data[1]

    def __Create(self, selection=[]):
        """Insertion des sélections dans la table des selections 
        """
        try:
            if not selection:
                return
            # Récupération des données dans la bdd
            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_selection = sqlalchemy.Table(
                'selection',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )
            with self.__instance.connect():
                lines = self.__instance.execute(
                    tInfo_selection.insert(None),
                    [
                        {
                            'id_project': self.__id_project,
                            'selection': aselection.selection,
                            'description': aselection.description,
                        } for aselection in selection
                    ]
                )

            FileLogger.log(
                logging.DEBUG, f"{lines.rowcount} selection(s) for project_ID: {self.__id_project} inserted!")
        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Read(self):
        """Lecture des selections pour un projet donné.
        """
        try:

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_selection = sqlalchemy.Table(
                'selection',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            dico_selection = {}
            with self.__instance.connect():

                query = sqlalchemy.select([tInfo_selection]).where(sqlalchemy.and_(
                    tInfo_selection.c.id_project == self.__id_project,)
                ).distinct()

                result = self.__instance.execute(query)

                if result.rowcount == 0:
                    return dico_selection
                for row in result:
                    aselection = selectionModel(
                        row[tInfo_selection.c.id_project],
                        row[tInfo_selection.c.selection],
                        row[tInfo_selection.c.description]
                    )
                    key = "{0}_#_{1}".format(
                        aselection.id_project, aselection.selection)

                    if not key in dico_selection:
                        dico_selection[key] = aselection

            return dico_selection

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Update(self, selection=[]):
        """Mise à jour des données dans la table selection
        """
        try:

            if selection == None:
                return

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_selection = sqlalchemy.Table(
                'selection',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            with self.__instance.connect():

                query = tInfo_selection.update(None).where(
                    sqlalchemy.and_(
                        tInfo_selection.c.id_project == int(self.__id_project),
                        tInfo_selection.c.selection == sqlalchemy.bindparam(
                            'c_selection'),
                    )
                ).values(
                    description=sqlalchemy.bindparam('description'),
                )

                lines = self.__instance.execute(query,
                                                [
                                                    {
                                                        'c_selection': str(aselection.selection),
                                                        'description': aselection.description,
                                                    } for aselection in selection
                                                ]
                                                )
            FileLogger.log(
                logging.DEBUG, f"{lines.rowcount} selection(s) for project_ID: {self.__id_project} updated!")

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def __Delete(self, selection=[]):
        """Suppression de selection(s).
        """
        try:

            metadata = sqlalchemy.MetaData(bind=None)
            tInfo_selection = sqlalchemy.Table(
                'selection',
                metadata,
                autoload=True,
                autoload_with=self.__connexion.engine()
            )

            with self.__instance.connect():
                lines = 0
                for aselection in selection:
                    selection = re.split(r'_#_', aselection)[1]
                    query = tInfo_selection.delete(None).where(
                        sqlalchemy.and_(
                            tInfo_selection.c.id_project == self.__id_project,
                            tInfo_selection.c.selection == selection
                        )
                    )
                    line = self.__instance.execute(query)
                    lines += int(line.rowcount)
            FileLogger.log(
                logging.DEBUG, f"{lines} selection(s) for project_ID: {self.__id_project} deleted!")

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def Execute(self):
        """Execution des traitements pour récupérer les selection d'un project_ID.
        """

        try:
            # Chargement de toutes les selections pour un project_ID.
            dict_selection = self.__Read()
            listUpdate_selection = []
            listInsert_selection = []
            listOfKeys = []
            selection_df = apex.retrieve_selection_list(
                self.__id_project, self.__project_ID, self.__api_KEY)
            for _i, row in selection_df.iterrows():
                aselection = selectionModel(
                    self.__id_project,
                    row["selection"],
                    row["description"],
                )

                currentKey = "{0}_#_{1}".format(
                    aselection.id_project, aselection.selection)

                if currentKey in listOfKeys:  # Si on a déjà traité cette clé.
                    continue
                listOfKeys.append(currentKey)
                if not currentKey in dict_selection:
                    listInsert_selection.append(aselection)
                else:
                    listUpdate_selection.append(aselection)
                    del dict_selection[currentKey]

            # Update
            if listUpdate_selection:
                FileLogger.log(
                    logging.DEBUG, f"Selection list for project_ID: {self.__id_project} Update in progress...")
                self.__Update(listUpdate_selection)

            # Delete
            if dict_selection:
                FileLogger.log(
                    logging.DEBUG, f"Selection list for project_ID: {self.__id_project} Delete in progress...")
                self.__Delete(dict_selection)

            # insert
            if listInsert_selection:
                FileLogger.log(
                    logging.DEBUG, f"Selection list for project_ID: {self.__id_project} Insert in progress...")
                self.__Create(listInsert_selection)

        except Exception:
            FileLogger.log(logging.ERROR, traceback.print_exc())

    def Close(self):
        self.__connexion.close()
        self.__instance.close()


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

select_selection_with_id_project = """
                            SELECT id_selection
                            FROM selection 
                            WHERE id_project=%s; 
                            """

select_selection_information = """
                                SELECT s.id_selection AS id, p.project_ID AS ID_p, 
                                    s.selection AS ID_s, s.description AS selection, 
                                    to_char(se.selection_extraction_date,'DD/MM/YY HH24:MI:SS') AS dernier_extract, 
                                    se.selection_extraction_nb_records AS Nb, 
                                    array_to_string(array_agg(c.category_name), ', ', '*') AS Catégorie,
                                    '' AS lancer, '' AS modifier
                                FROM selection AS s 
                                LEFT JOIN project AS p 
                                ON s.id_project=p.id_project
                                LEFT JOIN selection_category AS sc
                                ON s.id_selection=sc.id_selection
                                LEFT JOIN category AS c
                                ON sc.id_category=c.id_category
                                LEFT OUTER JOIN selection_extraction AS se 
                                ON s.id_selection = se.id_selection
                                AND se.selection_extraction_date =(
                                    SELECT MAX(selection_extraction_date) 
                                    FROM selection_extraction 
                                    WHERE id_selection=se.id_selection)
                                GROUP BY s.id_selection, p.project_ID, s.selection, s.description, 
                                    se.selection_extraction_date, se.selection_extraction_nb_records;
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
