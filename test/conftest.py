import pytest
from selenium import webdriver
from books_ui import BooksIU

# Фикстура для веб-драйвера
@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(4)
    yield driver
    driver.quit()  # Закрывает драйвер после всех тестов

# Фикстура для открытия главной страницы
@pytest.fixture()
def open_main_page(driver):
    driver.get("https://www.chitai-gorod.ru/")
    yield
    # Здесь можно добавить логику для выполнения после теста, если потребуется

# Фикстура для экземпляра BooksIU
@pytest.fixture()
def books_ui(driver, open_main_page):
    return BooksIU(driver)