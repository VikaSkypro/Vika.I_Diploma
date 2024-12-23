import allure
import pytest
from selenium import webdriver
from pages.books_ui import BooksIU
from pages.books_api import BooksApi

# Фикстуры UI
@pytest.fixture(scope='session')
def driver():
    """ Фикстура для веб-драйвера"""
    with allure.step("Открыть и настроить браузер"):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(4)
        yield driver
        driver.quit()


@pytest.fixture()
def open_main_page(driver):
    """Фикстура для открытия главной страницы Читай-город"""
    driver.get("https://www.chitai-gorod.ru/")
    yield


@pytest.fixture()
def books_ui(driver, open_main_page):
    """Фикстура для экземпляра BooksIU"""
    return BooksIU(driver)

# Фикстуры Api
@pytest.fixture(scope="class")
def shopping_books():
    url = "https://web-gate.chitai-gorod.ru"
    api = BooksApi(url)
    yield api