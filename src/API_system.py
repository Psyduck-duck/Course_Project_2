from abc import ABC, abstractmethod
import requests


class ApiConnection(ABC):
    """Абстрактный класс для работы с api ресурсами"""

    @abstractmethod
    def __init__(self):
        """Коструктор для определения основных параметров"""
        pass

    @abstractmethod
    def connect(self):
        """Метод для определения подключения к сервисам"""
        pass

    @abstractmethod
    def get_vacancy_data(self, search_text: str):
        """Метод для получения информации по вакансиям"""
        pass


class ApiConnectionHHRU(ApiConnection):
    """Класс для работы с API сервисами HH.ru"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {
            "text": None,
            "search_field": "name",
            "page": 0,
            "per_page": 100,
            "only_with_salary": False,
            "period": None,
        }
        self.__search_target = None
        self.__vacancies = []
        self.is_connecting = False

    def connect(self):
        pass

    def __connect_HHRU(self):
        """метод для определения установки связи c API HH.ru"""
        response = requests.get("https://api.hh.ru", self.__headers)
        if response.status_code != 200:
            raise ValueError("Check URL or headers")
        self.is_connecting = True

    def get_vacancy_data(self, search_text: str, per_page: int) -> list:
        """Метод для получения вакансий"""

        self.__connect_HHRU()
        if self.is_connecting:
            self.__headers["text"] = search_text
            self.__headers["per_page"] = per_page
            while self.__headers.get("page") != 20:
                response = requests.get(self.__url, self.__headers)
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__headers["page"] += 1

        else:
            raise ValueError("Connection status is False")

        return self.__vacancies
