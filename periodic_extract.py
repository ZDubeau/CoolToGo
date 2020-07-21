"""----------------------------
Creation date  : 2020-07-20
Last update    : 2020-07-21
----------------------------"""

import logging
from LoggerModule.FileLogger import FileLogger as FileLogger
from DB_Connexion import DB_connexion
import Table_project as prj
import app

if __name__ == "__main__":
    connexion = DB_connexion()
    project_list = connexion.Query_SQL_fetchall(prj.select_project_information)
    del connexion
    for project in project_list:
        project_id = project[0]
        app.asynchronous_selection_extract.apply_async(
            args=[project_id], countdown=2)
        FileLogger.log(
            logging.DEBUG, f"Periodic Task executed for project {project_id}")
