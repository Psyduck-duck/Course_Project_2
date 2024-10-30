import json
import os.path
import re
from abc import ABC, abstractmethod

from data.path_to_directory import PATH_TO_DATA_DIRECTORY
from src.vacancies import Vacancy


class FileWorker(ABC):
    """абстрактный класс для работы с файлами"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_file(self) -> None:
        pass

    @abstractmethod
    def add_data(self, vacancy_object: Vacancy) -> None:
        pass

    @abstractmethod
    def get_data(self, target_list: list) -> None:
        pass

    @abstractmethod
    def del_vacancy(self, id: str) -> None:
        pass


class FileWorkerJson(FileWorker):
    """класс для работы с файлом типа json"""

    def __init__(self, filename: str = "filename.json") -> None:
        """Конструктор для задачи параметров объекта"""

        self.__filename = filename
        self.__path_to_file = os.path.join(PATH_TO_DATA_DIRECTORY, self.__filename)
        self.__vacancy_data = []
        self.__id_list = []
        if self.is_file():
            with open(self.__path_to_file, "r", encoding="utf-8") as file:
                try:
                    vacancy_data = json.load(file)
                except ValueError:
                    vacancy_data = []
                if vacancy_data:
                    self.__vacancy_data = vacancy_data
                    for vacancy in vacancy_data:
                        self.__id_list.append(vacancy["id"])

    @property
    def filename(self) -> str:
        """геттер для получения имени файла для работы с данными"""

        return self.__filename

    @property
    def id_list(self) -> list[str]:
        """геттер для получения списка id вакансий в файле"""

        return self.__id_list

    def is_file(self) -> bool:
        """проверяет существует ли файл"""

        try:
            with open(self.__path_to_file, "r", encoding="utf-8"):
                return True
        except FileNotFoundError:
            return False

    def create_file(self) -> None:
        """метод для создания файла"""

        if self.is_file():
            raise ValueError("File already is")
        with open(self.__path_to_file, "w", encoding="utf-8"):
            pass

    def get_data(self, target_list: list) -> list[Vacancy]:
        """метод для получения данных из файла по ключевым словам"""

        target_list = [x.lower() for x in target_list]
        pattern_list = [re.compile(rf"{i}") for i in target_list]
        mathed_vacancies_list = []
        for vacancy in self.__vacancy_data:
            is_match = False
            for pat in pattern_list:
                for value in vacancy.values():
                    if type(value) == str:
                        math = re.findall(pat, value.lower())
                        if math:
                            is_match = True
                    if type(value) == dict:
                        for val in value.values():
                            if type(val) == str:
                                match = re.findall(pat, val.lower())
                                if match:
                                    is_match = True

            if is_match:
                mathed_vacancies_list.append(vacancy)

        return mathed_vacancies_list

    def add_data(self, vacancy_object: Vacancy) -> None | bool:
        """метод для добавления уникальной вакансии"""

        if self.is_file():
            if vacancy_object.id not in self.__id_list:
                with open(self.__path_to_file, "r+", encoding="utf-8") as file:

                    vacancy_object_dict = {
                        "id": vacancy_object.id,
                        "name": vacancy_object.name,
                        "salary": {
                            "from": vacancy_object.salary_down,
                            "to": vacancy_object.salary_up,
                            "currency": vacancy_object.salary_currency,
                        },
                        "alternate_url": vacancy_object.url,
                        "snippet": {
                            "requirement": vacancy_object.requirement,
                            "responsibility": vacancy_object.responsibility,
                        },
                    }
                    self.__vacancy_data.append(vacancy_object_dict)
                    json.dump(self.__vacancy_data, file, indent=4, ensure_ascii=False)
                    self.__id_list.append(vacancy_object.id)
            else:
                return False
        else:
            print("Create file!")

    def del_vacancy(self, id: str) -> None:
        """Метод для удаления вакансии из файла по ID"""

        for vacancy in self.__vacancy_data:
            if vacancy["id"] == id:
                self.__vacancy_data.remove(vacancy)
                self.__id_list.remove(id)
                with open(self.__path_to_file, "w", encoding="utf-8") as file:
                    json.dump(self.__vacancy_data, file, indent=4, ensure_ascii=False)

    def get_top_n(self, n: int) -> list:
        """Метод для предоставления топ объектов по зарплате"""

        vacancy_list = self.__vacancy_data
        new_vacansy_list = []
        for vacany in vacancy_list:
            if vacany.get("salary").get("from"):
                new_vacansy_list.append(vacany)
        sorted_vacancy_list = sorted(new_vacansy_list, key=lambda x: x["salary"]["from"], reverse=True)

        return sorted_vacancy_list[0 : (n + 1)]
