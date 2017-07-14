#######################################################
# 
# abstract_file_reader.py
# Python implementation of the Class SensorFileReader
# Generated by Enterprise Architect
# Created on:      09-Jul-2017 21:09:12
# Original author: Laptop
# 
#######################################################
from abc import abstractmethod
from datetime import datetime

import sensor_file.file_parser.concrete_file_parser as file_parser
from sensor_file.domain.records import Record
from sensor_file.domain.site import Site

TXT_FILE_TYPES = ('dat', 'lev', 'xle')
XLS_FILES_TYPES = ('xls', 'xlsx')
CSV_FILES_TYPES = ('csv')


class AbstractFileReader(object):
    """Interface permettant de lire un fichier provenant d'un datalogger quelconque
    classe permettant d'extraire des données d'un fichier quelconque.
    Un fichier de donnée est en général composé de :
    - Entete d'information sur l'environnement de prise de données
    - Entete d'information sur les colonnes de données
    - Les colonnes de données
    """

    def __init__(self, file_name: str = None, header_length: int = 10):
        self._file = file_name
        self._header_length = header_length
        self._site_of_interest = None
        self.file_reader = None
        self._set_file_reader()

    def _set_file_reader(self):
        """
        set the good file parser to open and read the provided file
        :return:
        """
        file_ext = self.get_file_extension
        if file_ext in TXT_FILE_TYPES:
            self.file_reader = file_parser.TXTFileParser(self._file, self._header_length)
        elif file_ext in XLS_FILES_TYPES:
            self.file_reader = file_parser.EXCELFileParser(self._file, self._header_length)
        elif file_ext in CSV_FILES_TYPES:
            self.file_reader = file_parser.CSVFileParser(self._file, self._header_length)

    @property
    def get_file_extension(self):
        file_list = self._file.split(".")
        if len(file_list) == 1:
            raise ValueError("The path given doesn't point to a file name")
        if len(file_list) > 2:
            raise ValueError("The file name seems to be corrupted. Too much file extension in the current name")
        else:
            return file_list[-1].lower()

    def _make_site(self):
        self.read_file_header()
        self.read_file_data_header()

    def _make_data(self):
        self.read_file_data()

    @abstractmethod
    def read_file_header(self):
        """
        Methode permettant de lire l'entete du fichier
        :return:
        """
        pass

    @abstractmethod
    def read_file_data_header(self):
        """
        Methode permettant de lire l'entete des colonnes de donnees (information sur ce qui est enregistré/mesuré)
        :return:
        """
        pass

    @abstractmethod
    def read_file_data(self):
        """
        Methode pour ne recupérer que les données du fichier
        :return:
        """
        pass
