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
    def add_data(self, vacancy_object):
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

        self.__filename = filename
        self.__path_to_file = os.path.join(PATH_TO_DATA_DIRECTORY, self.__filename)
        self.__urls_list = []
        if self.is_file():
            with open(self.filename, "r", encoding="utf-8") as file:
                vacancy_data = json.load(file)
                for vacancy in vacancy_data:
                    self.__urls_list.append(vacancy.url)

    @property
    def filename(self):
        """геттер для получения имени файла для работы с данными"""

        return self.__filename

    def is_file(self):
        """проверяет существует ли файл"""

        try:
            with open(self.__path_to_file, "r", encoding="utf-8"):
                return True
        except FileNotFoundError:
            return False

    def create_file(self):
        """метод для создания файла"""

        if self.is_file():
            raise ValueError("File already is")
        with open(self.__path_to_file, "w", encoding="utf-8"):
            pass

    def get_data(self):
        """метод для получения данных из файла"""

        self.__vacancy_data = []
        with open(self.__filename, "r", encoding="utf-8") as file:
            self.__data = json.load(file)

    def add_data(self, vacancy_object):
        """метод для добавления уникальной вакансии"""

        if self.is_file():

            with open(self.__filename, "a", encoding="utf-8") as file:
            # Добавлять элементы и параллельно добавлять юрл в список юрлов, если такой юрс уже существует,
            # пропускать вакансию
                if not vacancy_object.url in self.__urls_list:
                    json.dump(vacancy_object, file, indent=4, ensure_ascii=False)
                    self.__urls_list.append(vacancy_object.url)
                else:
                    return False
        else:
            print("Create file!")
