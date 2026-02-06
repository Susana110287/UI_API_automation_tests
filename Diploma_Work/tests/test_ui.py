import allure
import pytest
from selenium import webdriver
from ExtendedSearchUI import ExtendedSearchUI


@pytest.fixture
def driver():
    """Фикстура для инициализации браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@allure.feature("Расширенный поиск на Кинопоиске")
class TestExtendedSearch:

    @allure.story("1. Поиск по названию фильма")
    def test_search_by_title(self, driver):
        search_page = ExtendedSearchUI(driver)

        with allure.step("1. Открытие страницы расширенного поиска"):
            search_page.open_advanced_search()

        with allure.step("2. Ввод названия фильма"):
            search_page.set_film_title("Матрица")

        with allure.step("3. Нажатие кнопки поиска"):
            search_page.click_search_movies()

        with allure.step("4. Проверка результатов"):
            results_count = search_page.get_movie_results_count()
            assert results_count > 0, "Нет результатов по запросу"

            # Дополнительно проверяем наличие ключевого слова в результатах
            page_text = driver.page_source.lower()
            assert "матрица" in page_text, "Название фильма не найдено в результатах"

    @allure.story("2. Поиск по стране")
    def test_search_by_country(self, driver):
        search_page = ExtendedSearchUI(driver)

        with allure.step("1. Открытие страницы расширенного поиска"):
            search_page.open_advanced_search()

        with allure.step("2. Выбор страны в выпадающем списке"):
            search_page.select_country("Россия")

        with allure.step("3. Нажатие кнопки поиска"):
            search_page.click_search_movies()

        with allure.step("4. Проверка результатов"):
            # 4.1. Проверка отображения выбранной страны в результатах
            assert search_page.is_country_displayed("Россия"), \
                "Страна «Россия» не отображается в результатах (элемент <span class='text-blue'>)"

            # 4.2. Проверка счётчика результатов (число > 0)
            results_count = search_page.get_results_count()
            assert results_count > 0, \
                f"Количество результатов равно {results_count}. Ожидалось число > 0"

            # 4.3. Дополнительная проверка формата счётчика
            count_text = search_page.get_results_count_text()
            assert count_text == f"({results_count})", \
                f"Формат счётчика не соответствует ожидаемому. Получено: {count_text}, ожидалось: ({results_count})"

    @allure.story("3. Поиск по году")
    def test_search_by_year(self, driver):
        search_page = ExtendedSearchUI(driver)

        with allure.step("1. Открытие страницы расширенного поиска"):
            search_page.open_advanced_search()

        with allure.step("2. Ввод года"):
            search_page.set_year("2020")

        with allure.step("3. Нажатие кнопки поиска"):
            search_page.click_search_movies()

        with allure.step("4. Проверка результатов"):
            results_count = search_page.get_movie_results_count()
            assert results_count > 0, "Нет результатов по запросу"

            # Проверим, что год присутствует в HTML
            page_text = driver.page_source
            assert "2020" in page_text, "Год не найден в результатах"

    @allure.story("4. Поиск по жанру")
    def test_search_by_genre(self, driver):
        search_page = ExtendedSearchUI(driver)

        with allure.step("1. Открытие страницы расширенного поиска"):
            search_page.open_advanced_search()

        with allure.step("2. Выбор жанров"):
            search_page.select_genres(["фантастика", "приключения"])  # Исправлено: select_genres → select_genres

        with allure.step("3. Нажатие кнопки поиска"):
            search_page.click_search_movies()

        with allure.step("4. Проверка результатов"):
            results_count = search_page.get_movie_results_count()
            assert results_count > 0, "Нет результатов по запросу"

            # Проверим наличие жанров в HTML
            page_text = driver.page_source.lower()
            assert "фантастика" in page_text, "Жанр «фантастика» не найден"
            assert "приключения" in page_text, "Жанр «приключения» не найден"

    @allure.story("5. Поиск по актёру")
    @allure.title("Поиск актёра: {actor_name}")
    @pytest.mark.parametrize("actor_name", [
        "Киану Ривз",
        "Александр Устюгов",
        "Том Хэнкс"
    ])
    def test_search_by_actor(self, driver, actor_name):
        """
        Тест: поиск актёра по имени с проверкой:
        - в заголовке персональной страницы;
        - в строке результатов поиска.
        """
        search_page = ExtendedSearchUI(driver)

        with allure.step("1. Открытие страницы поиска людей"):
            driver.get("https://www.kinopoisk.ru/s/people/")

        with allure.step(f"2. Ввод имени актёра: {actor_name}"):
            search_page.set_actor_name(actor_name)

        with allure.step("3. Нажатие кнопки поиска актёров"):
            search_page.click_search_actors()

        with allure.step("4. Проверка результатов"):
            # Проверяем, что хотя бы один из критериев выполнен
            is_found = search_page.is_actor_in_results(actor_name)
            assert is_found, f"Актёр «{actor_name}» не найден в результатах поиска"
