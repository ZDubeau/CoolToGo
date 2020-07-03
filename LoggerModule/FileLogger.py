import logging
import logging.config
import os


class FileLogger:
    """Classe qui initialise un logger
    """
    _logger = None

    @staticmethod
    def InitLogger():
        """Initialise un logger à partir du fichier de config par défaut.
        Ce fichier doit être contenu dans le même dossier que le module
        Logger
        """
        # Configuration de logging.
        try:
            # Configuration par fichier pour logging
            logging.config.fileConfig(
                fname='logging.conf'
            )
            FileLogger._logger = logging.getLogger('Schneider')
        except Exception:
            # Si le fichier n'est pas trouvé alors on fait une configuration basique.
            logging.basicConfig(
                level=logging.DEBUG,
                filename='default.log',
                filemode='a',
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            # initialisation d'un logger par défaut.
            FileLogger._logger = logging.getLogger(None)

    @staticmethod
    def InitLoggerByFile(path, loggerName):
        try:

            # On vérifie que le fichier existe.
            if not os.path.exists(path):
                raise FileNotFoundError(
                    "Your logger file config does not exist!")

            # le fichier existe on initialise notre logger.
            logging.config.fileConfig(
                fname=path
            )
            FileLogger._logger = logging.getLogger(loggerName)
        except Exception as ex:
            # pas grave si on a pas pu initialiser le logger.
            logging.debug("Could not initialize the logger!")

    @staticmethod
    def log(niveau, message, exc_info=False):
        if FileLogger._logger == None:
            print(message)  # On print sur la console.None
        else:
            FileLogger._logger.log(niveau, message, exc_info=exc_info)
