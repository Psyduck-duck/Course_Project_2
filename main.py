from src.API_system import ApiConnectionHHRU


example = ApiConnectionHHRU()
data = example.get_vacancy_data("Python", 1)
for i in data:
    print(i)