import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    # Настройки Chrome
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Создание драйвера
    driver = webdriver.Chrome(options=options)
    yield driver  # Передаём драйвер в тест
    # Закрытие драйвера после теста
    driver.quit()
