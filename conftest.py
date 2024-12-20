import pytest
from selenium import webdriver
from books_ui import BooksIU


# Фикстура для веб-драйвера
@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(4)
    driver.get("https://www.chitai-gorod.ru/")
    yield driver
    driver.quit()  # Закрывает драйвер после теста


# Фикстура для экземпляра BooksIU
@pytest.fixture()
def books_ui(driver):
    return BooksIU(driver)  # Возвращаем экземпляр BooksIU с переданным драйвером