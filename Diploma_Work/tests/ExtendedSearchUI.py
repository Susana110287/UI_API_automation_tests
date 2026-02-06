from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure


class ExtendedSearchUI:
    """Класс для взаимодействия с формами расширенного поиска на Кинопоиске."""

    def __init__(self, driver):
        self._driver = driver

    def open_advanced_search(self):
        """Открыть страницу расширенного поиска."""
        self._driver.get("https://www.kinopoisk.ru/s/advanced/")

    def set_film_title(self, title: str):
        """Ввести название фильма в поле поиска."""
        with allure.step(f"Ввод названия фильма: {title}"):
            film_input = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.ID, "find_film"))
            )
            film_input.clear()
            film_input.send_keys(title)

    def select_country(self, country_name: str):
        """Выбрать страну из выпадающего списка."""
        with allure.step(f"Выбор страны: {country_name}"):
            country_select = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.ID, "country"))
            )
            select = Select(country_select)
            select.select_by_visible_text(country_name)

    def set_year(self, year: str):
        """Ввести год в поле «Год»."""
        with allure.step(f"Ввод года: {year}"):
            year_input = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.ID, "year"))
            )
            year_input.clear()
            year_input.send_keys(year)

    def select_genres(self, genre_names: list):
        """Выбрать жанры (можно несколько)."""
        with allure.step(f"Выбор жанров: {genre_names}"):
            genre_select = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.ID, "m_act[genre]"))
            )
            select = Select(genre_select)
            for genre in genre_names:
                select.select_by_visible_text(genre)

    def set_actor_name(self, name: str):
        """Ввести имя актёра в поле поиска."""
        with allure.step(f"Ввод имени актёра: {name}"):
            actor_input = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.ID, "find_people"))
            )
            actor_input.clear()
            actor_input.send_keys(name)

    def click_search_movies(self):
        """Нажать кнопку «Поиск» для фильмов."""
        with allure.step("Нажатие кнопки поиска фильмов"):
            search_button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//input[@class='el_18 submit nice_button' and @value='поиск']"
                ))
            )
            search_button.click()

    def click_search_actors(self):
        """Нажать кнопку «Поиск» для актёров."""
        with allure.step("Нажатие кнопки поиска актёров"):
            search_button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//input[@class='el_8 submit nice_button' and @value='поиск']"
                ))
            )
            search_button.click()

    def wait_for_movie_results(self, timeout=15) -> list:
        """Дождаться результатов поиска фильмов и вернуть элементы."""
        with allure.step("Ожидание результатов поиска фильмов"):
            WebDriverWait(self._driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search_results"))
            )
            return self._driver.find_elements(By.CSS_SELECTOR, "div.search_results div.element")

    def get_movie_results_count(self) -> int:
        """Получить количество найденных фильмов."""
        results = self.wait_for_movie_results()
        return len(results)

    def is_country_displayed(self, country: str) -> bool:
        """
        Проверить, что выбранная страна отображается в результатах.
        """
        try:
            element = WebDriverWait(self._driver, 5).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    f"//span[@class='text-blue' and text()='«{country}»']"
                ))
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_results_count(self) -> int:
        """
        Получить число результатов из элемента.
        Возвращает целое число или 0, если элемент не найден.
        """
        try:
            count_element = WebDriverWait(self._driver, 5).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "font[color='#0000555']"
                ))
            )
            text = count_element.text.strip()
            # Извлекаем число из формата "(34192)"
            if text.startswith("(") and text.endswith(")"):
                return int(text[1:-1])
            return 0
        except (TimeoutException, NoSuchElementException, ValueError):
            return 0

    def get_results_count_text(self) -> str:
        """Получить текст с количеством результатов (например, (34192))."""
        try:
            count_element = WebDriverWait(self._driver, 5).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "font[color='#0000555']"
                ))
            )
            return count_element.text
        except (TimeoutException, NoSuchElementException):
            return ""

    def is_actor_in_results(self, name: str) -> bool:
        """
        Проверить, что актёр присутствует в результатах:
        1. В заголовке <h1> на персональной странице.
        2. В строке поиска результатов <span class="search_results_topText">.
        """
        try:
            # 1. Проверка заголовка <h1> (персональная страница актёра)
            h1_element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "h1.styles_primaryName__LB_CC.styles_root__krgW7.styles_rootInLight__8xmQ4[data-tid='f22e0093']"
                ))
            )
            if name.lower() in h1_element.text.lower():
                return True

        except TimeoutException:
            pass  # h1 не найден — проверяем второй вариант

        try:
            # 2. Проверка строки результатов поиска
            top_text_element = WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "span.search_results_topText"
                ))
            )
            if name.lower() in top_text_element.text.lower():
                return True

        except TimeoutException:
            pass  # top_text не найден

        return False  # ни один из критериев
