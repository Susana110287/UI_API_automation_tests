import allure
import requests
import pytest
from config import API_BASE_URL, API_TOKEN


# Тест №1 "Поиск фильма по названию"
@allure.feature("API: Поиск")
@allure.story("Поиск фильма по названию")
@pytest.mark.api
def test_search_movie_by_title():
    headers = {"X-API-KEY": API_TOKEN}
    params = {"query": "Мумия", "page": 1, "limit": 5}

    with allure.step("Сформировать URL для запроса"):
        url = f"{API_BASE_URL}/movie"

    with allure.step("Отправить GET‑запрос на поиск фильма"):
        response = requests.get(
            url, headers=headers, params=params, timeout=10
        )

    with allure.step("Проверить статус ответа (ожидается 200 OK)"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"


# Тест №2 "Поиск фильма по жанру и году"
@allure.feature("API: Поиск")
@allure.story("Поиск фильма по жанру и году")
@pytest.mark.api
def test_search_movie_by_genre_and_year():
    headers = {"X-API-KEY": API_TOKEN}
    # Параметры поиска: жанр и год
    params = {
        "genres.name": "фантастика",  # название жанра
        "year": 2020,              # год выпуска
        "page": 1,
        "limit": 5
    }

    with allure.step("Сформировать URL для запроса"):
        url = f"{API_BASE_URL}/movie"

    with allure.step("Отправить GET‑запрос на поиск фильма по жанру и году"):
        response = requests.get(
            url, headers=headers, params=params, timeout=10
        )

    with allure.step("Проверить статус ответа (ожидается 200 OK)"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"


# Тест №3 "Поиск фильма с актёром"
@allure.feature("API: Поиск")
@allure.story("Поиск фильма с актёром")
@pytest.mark.api
def test_search_movie_by_actor():
    headers = {"X-API-KEY": API_TOKEN}
    # Параметр поиска — имя актёра (можно задать любое значение)
    params = {
        "query": "Том Хэнкс",  # имя актёра
        "page": 1,
        "limit": 5
    }

    with allure.step("Сформировать URL для запроса"):
        url = f"{API_BASE_URL}/movie"

    with allure.step("Отправить GET‑запрос на поиск фильма с актёром"):
        response = requests.get(
            url, headers=headers, params=params, timeout=10
        )

    with allure.step("Проверить статус ответа (ожидается 200 OK)"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"


# Тест №4 "Поиск фильма по возрастному рейтингу"
@allure.feature("API: Поиск")
@allure.story("Поиск фильма по возрастному рейтингу")
@pytest.mark.api
def test_search_movie_by_age_rating():
    headers = {"X-API-KEY": API_TOKEN}
    # Параметр поиска — возрастной рейтинг
    params = {
        "ageRating": "18",  # возрастной рейтинг
        "page": 1,
        "limit": 5
    }

    with allure.step("Сформировать URL для запроса"):
        url = f"{API_BASE_URL}/movie"

    with allure.step(
        "Отправить GET‑запрос на поиск фильма по возрастному рейтингу"
    ):
        response = requests.get(
            url, headers=headers, params=params, timeout=10
        )

    with allure.step("Проверить статус ответа (ожидается 200 OK)"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"


# Тест №5 "Поиск фильма с пустым запросом"
@allure.feature("API: Поиск")
@allure.story("Поиск фильма с пустым запросом")
@pytest.mark.api
def test_search_movie_with_empty_query():
    headers = {"X-API-KEY": API_TOKEN}
    # Параметры поиска с пустым значением query
    params = {
        "query": "",          # пустой запрос
        "page": 1,
        "limit": 5
    }

    with allure.step("Сформировать URL для запроса"):
        url = f"{API_BASE_URL}/movie"

    with allure.step("Отправить GET‑запрос с пустым параметром query"):
        response = requests.get(
            url, headers=headers, params=params, timeout=10
        )

    with allure.step("Проверить статус ответа (ожидается 400 или 401)"):
        assert response.status_code in [400, 401], \
            (f"Ожидался статус 400 (Bad Request) или 401 (Unauthorized), "
             f"получен {response.status_code}")
