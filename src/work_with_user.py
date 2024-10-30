from src.API_system import ApiConnectionHHRU
from src.filework import FileWorkerJson
from src.vacancies import VacancyHHRU


def work_with_user():
    """Функция для взаимодействия с пользотелем"""

    print("Добро пожаловать в поисковую систему по вакансиям с HH.ru")
    print()
    search_name = input("Введите ваш запрос: ")
    api_object = ApiConnectionHHRU()
    vacancies_list = api_object.get_vacancy_data(search_name, 100)
    vacancies_objects_list = [VacancyHHRU(vacancy) for vacancy in vacancies_list]
    filename = search_name.replace(" ", "_")
    fileworker_object = FileWorkerJson(f"{filename}.json")
    if not fileworker_object.is_file():
        fileworker_object.create_file()
    for x in vacancies_objects_list:
        fileworker_object.add_data(x)

    users_answer = None
    while users_answer not in ["yes", "y", "no", "n"]:
        users_answer = input("Хотите получить топ по зарплате?: ").lower()
        if users_answer in ["yes", "y"]:
            num_for_top = None
            while type(num_for_top) != int:
                try:
                    num_for_top = int(input("Введите число для количества вакансий в топе: "))
                except Exception:
                    print("Введите число")
                    num_for_top = None
            top_list = fileworker_object.get_top_n(num_for_top)
            for x in top_list:
                print(x)
        elif users_answer in ["no", "n"]:
            pass
        else:
            print("Ваш ответ не ясен")

    user_answer_for_search = None
    while user_answer_for_search not in ["yes", "y", "no", "n"]:
        user_answer_for_search = input("Хотите получить вакансии по ключевым словам?: ").lower()
        if user_answer_for_search in ["yes", "y"]:
            user_pattern = input("Введите ключевые слова через запятую: ").lower()
            user_pattern_list = user_pattern.split(", ")
            result = fileworker_object.get_data(user_pattern_list)
            for x in result:
                print(x)
        elif users_answer in ["no", "n"]:
            pass
        else:
            print("Ваш ответ не ясен")
