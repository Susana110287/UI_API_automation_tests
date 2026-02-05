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
