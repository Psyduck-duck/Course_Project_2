from abc import ABC, abstractmethod
import requests


class ApiConnection(ABC):
    """ Абстрактный класс для работы с api ресурсами"""

    @abstractmethod
    def __init__(self):
        """Коструктор для определения основных параметров"""
        self.search_target = None
        self.url = None
        self.headers = None
        self.is_connecting = False

    def connect(self):
        """Метод для определения подключения к сервисам"""
        response = requests.get(self.url, self.headers)
        if response.status_code != 200:
            raise ValueError("Check URL or headers")
        self.is_connecting = True

    def define_search_target(self, search_text):
        self.search_target = search_text

    @property
    def vacancy_data(self):
        """Метод - геттер для получения информации по вакансиям"""

        if self.is_connecting:
            response = requests.get(self.url, self.headers)
            data = response.json()

            return data

        else:
            raise ValueError("Connection status is False")


class ApiConnectionHHRU(ApiConnection):
    """Класс для работы с API сервисами HH.ru"""

    def __init__(self):
        super().__init__()
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {
            "text": None,
            "search_field": "name",
            "page": 0,
            "per_page": 100,
            "only_with_salary": True,
            "period": 1,
        }

    def