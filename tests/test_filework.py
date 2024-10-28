import json
import os

import pytest

from data.path_to_directory import PATH_TO_DATA_DIRECTORY
from src.filework import FileWorkerJson
from src.vacancies import VacancyHHRU


@pytest.fixture
def vacancy_object():
    return VacancyHHRU(
        {
            "id": "1",
            "name": "test",
            "salary": {
                "from": 1,
                "to": 2,
                "currency": "ANT",
            },
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        }
    )


@pytest.fixture
def vacancy_object_2():
    return VacancyHHRU(
        {
            "id": "2",
            "name": "Python",
            "salary": {
                "from": 1,
                "to": 2,
                "currency": "test",
            },
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        }
    )


def test_FileWorkerJson():
    object = FileWorkerJson("test.json")
    # object.create_file()   #создаст файл только если он не существует
    with pytest.raises(ValueError):
        object.create_file()
    assert object.is_file() == True


def test_FileWorkerJson_add_data(vacancy_object, vacancy_object_2):
    object = FileWorkerJson("test_2.json")
    # object.create_file()
    object.add_data(vacancy_object)
    object.add_data(vacancy_object)
    object.add_data(vacancy_object)
    object.add_data(vacancy_object_2)
    object.add_data(vacancy_object_2)

    with open(os.path.join(PATH_TO_DATA_DIRECTORY, "test_2.json")) as file:
        data = json.load(file)
        assert data == [
            {
                "id": "1",
                "name": "test",
                "salary": {"from": 1, "to": 2, "currency": "ANT"},
                "alternate_url": "https://test.ru",
                "snippet": {"requirement": "test", "responsibility": "test"},
            },
            {
                "id": "2",
                "name": "Python",
                "salary": {"from": 1, "to": 2, "currency": "test"},
                "alternate_url": "https://test.ru",
                "snippet": {"requirement": "test", "responsibility": "test"},
            },
        ]

    assert object.id_list == ["1", "2"]

    object_2 = FileWorkerJson("test_2.json")
    assert object_2.id_list == ["1", "2"]


def test_FileWorkerJson_without_file(capsys, vacancy_object):
    object = FileWorkerJson("nothing.json")

    assert object.is_file() == False

    object.add_data(vacancy_object)

    message = capsys.readouterr()
    assert message.out.strip() == "Create file!"


def test_FileWorkerJson_get_data():

    object = FileWorkerJson("test_2.json")
    assert object.get_data(["python", "aNt"]) == [
        {
            "id": "1",
            "name": "test",
            "salary": {"from": 1, "to": 2, "currency": "ANT"},
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        },
        {
            "id": "2",
            "name": "Python",
            "salary": {"from": 1, "to": 2, "currency": "test"},
            "alternate_url": "https://test.ru",
            "snippet": {"requirement": "test", "responsibility": "test"},
        }
    ]
