import pytest
from selenium import webdriver
from pages.books_ui import BooksIU


@pytest.fixture(scope='session')
def driver():
    """ Фикстура для веб-драйвера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(4)
    yield driver
    driver.quit()  # Закрывает драйвер после всех тестов


@pytest.fixture()
def open_main_page(driver):
    """Фикстура для открытия главной страницы Читай-город"""
    driver.get("https://www.chitai-gorod.ru/")
    yield


@pytest.fixture()
def books_ui(driver, open_main_page):
    """Фикстура для экземпляра BooksIU"""
    return BooksIU(driver)
