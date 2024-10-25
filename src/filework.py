import os.path
from abc import ABC, abstractmethod

import json

from data.path_to_directory import PATH_TO_DATA_DIRECTORY


class FileCreator(ABC):
    """абстрактный класс для работы с файлами"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_file(self):
        pass

    @abstractmethod
    def add_data(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def del_data(self):
        pass


class FileCreatorJson(FileCreator):
    """класс для работы с файлом типа json"""


    def __init__(self, filename = "filename.json"):
        """Конструктор для задачи параметров объекта"""

        self.filename = filename
        self.path_to_file = os.path.join(PATH_TO_DATA_DIRECTORY, self.filename)

    def create_file(self):
        """метод для создания файла"""

        with open(self.path_to_file, "w", encoding="utf-8"):
            pass

    def get_data(self):
        """метод для получения данных из файла"""

        self.vacancy_data = []
        with open(self.filename, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def add_data(self, vacancy_objects):
        """метод для добавления уникальной вакансии"""

        with open(self.filename, "a", encoding="utf-8") as file:
            pass



