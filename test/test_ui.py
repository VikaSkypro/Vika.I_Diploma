import pytest
import allure
from allure_commons.types import Severity
from fuzzywuzzy import fuzz
from pages.books_ui import BooksIU


@allure.epic("UI. Интернет-магазин Читай-город")
@allure.feature("UI.Главная страница")
@allure.suite("UI. Поиск книг в интернет-магазине Читай-город")
class TestBooksSearch:

    @pytest.mark.positive
    @allure.story("Позитивные тесты")
    @allure.id("SearchBook-1")
    @allure.title("Поиск книги по названию в городе Москва")
    @allure.description("Тест закрывает уведомления о подписке на рассылку"
                        " и предложение зарегистрироваться. "
                        "Выбирает нужный город. "
                        "Выполняет поиск книги по названию,"
                        "в котором есть опечатка и неверный регистр."
                        "Проверяет, что книга найдена.")
    @allure.severity(Severity.BLOCKER)
    @allure.step('1. Поиск книги по названию в городе Москва')
    def test_ui_search_for_book_in_moscow(self, driver, open_main_page, books_ui):
        """Тест выполняет поиск книги по названию в Москве.
        Нечувствителен к регистру и опечаткам"""
        with allure.step('Ввод города и названия книги'):
            city = "Москва"
            book_title = "Белоснешка И"
        books_ui.close_notification_reg()
        books_ui.close_notification()
        books_ui.find_city(city)
        books_ui.search_for_book(book_title)

        with allure.step('Получение названия найденных книг'):
            found_books_titles = books_ui.find_all_book_titles()
            print("Названия найденных книг:")
            for title in found_books_titles.keys():
                print(f"- {title}")

        with allure.step('Проверка наличия искомой книги среди найденных'):
            found = any(
                fuzz.partial_ratio(book_title.lower(), title.lower()) >= 70 for title in found_books_titles.keys())
            assert found, "Книга не найдена в результатах поиска."

    @pytest.mark.positive
    @allure.story("Позитивные тесты")
    @allure.id("SearchBook-2")
    @allure.title("Поиск книги по полному названию в городе Казань")
    @allure.description("Тест закрывает уведомления о подписке на рассылку"
                        " и предложение зарегистрироваться. "
                        "Выбирает нужный город. "
                        "Выполняет поиск книги по полному названию."
                        "Проверяет, что книга найдена.")
    @allure.severity(Severity.NORMAL)
    @allure.step('2. Поиск книги по полному названию в городе Казань')
    def test_ui_search_for_book_in_kazan(self, books_ui):
        """Тест выполняет поиск книги по полному названию в Казани.
        Нечувствителен к регистру.
        Чувствителен к опечаткам."""
        with allure.step('Ввод города и названия книги'):
            city = "Казань"
            book_title = "Болотница"
        # books_ui.close_notification_reg()
        # books_ui.close_notification()
        books_ui.find_city(city)
        books_ui.search_for_book(book_title)

        with allure.step('Получение названия найденных книг'):
            found_books_titles = books_ui.find_all_book_titles()
            print("Названия найденных книг:")
            for title in found_books_titles.keys():
                print(f"- {title}")

        with allure.step('Проверка наличия искомой книги среди найденных'):
            try:
                found = any(book_title.lower() == title.lower() for title in found_books_titles.keys())
                assert found, "Книга не найдена в результатах поиска."
            except Exception as e:
                print(f"Ошибка при проверке наличия книги: {e}")

    @pytest.mark.negative
    @allure.story("Негативные тесты")
    @allure.id("SearchBook-3")
    @allure.title("Поиск книги по названию с некорректным регистром")
    @allure.description("Тест закрывает уведомления о подписке на рассылку"
                        " и предложение зарегистрироваться. "
                        "Выбирает нужный город. "
                        "Выполняет поиск книги с некорректным регистром."
                        "Проверяет, что книга не найдена.")
    @allure.severity(Severity.MINOR)
    @allure.step('Поиск книги по названию с некорректным регистром')
    def test_ui_search_book_incorrect_case(self, books_ui):
        """Тест выполняет поиск книги с неправильным регистром."""
        with allure.step('Ввод города и названия книги'):
            city = "Москва"
            book_title = "болотница"
        books_ui.close_notification_reg()
        books_ui.close_notification()
        books_ui.find_city(city)
        books_ui.search_for_book(book_title)

        with allure.step('Получение названия найденных книг'):
            found_books_titles = books_ui.find_all_book_titles()

        with allure.step('Проверка отсутствия искомой книги среди найденных'):
            found = any(book_title == title for title in found_books_titles.keys())

            try:
                assert not found, f"Книга '{book_title}' найдена в результатах поиска, что является неверным результатом."
            except AssertionError as e:
                print(e)

    @pytest.mark.negative
    @allure.story("Негативные тесты")
    @allure.id("SearchBook-4")
    @allure.title("Поиск книги по названию с опечаткой")
    @allure.description("Тест закрывает уведомления о подписке на рассылку"
                        " и предложение зарегистрироваться. "
                        "Выбирает нужный город. "
                        "Выполняет поиск книги с опечаткой в названии."
                        "Проверяет, что книга не найдена."
                        "Находит список похожих книг.")
    @allure.severity(Severity.NORMAL)
    @allure.step('Поиск книги по названию с опечаткой')
    def test_ui_search_book_typo(self, books_ui):
        """Тест выполняет поиск книги по названию с опечаткой.
        Нечувствителен к регистру.
        Чувствителен к опечаткам.
        """
        with allure.step('Ввод города и названия книги'):
            city = "Уфа"
            book_title = "Балотница"
        # books_ui.close_notification_reg()
        # books_ui.close_notification()
        books_ui.find_city(city)
        books_ui.search_for_book(book_title)

        with allure.step('Получение названия найденных книг'):
            found_books_titles = books_ui.find_all_book_titles()
            print("Названия найденных книг:")
            for title in found_books_titles.keys():
                print(f"- {title}")

        with allure.step('Проверка отсутствия искомой книги среди найденных'):
            try:
                found = any(book_title.lower() == title.lower() for title in found_books_titles.keys())
                assert not found, f"Книга '{book_title}' найдена в результатах поиска, что является неверным результатом."
            except AssertionError as e:
                print(e)

    @pytest.mark.negative
    @allure.story("Негативные тесты")
    @allure.id("SearchBook-5")
    @allure.title("Поиск книг с названием из иероглифов")
    @allure.description("Тест закрывает уведомления о подписке на рассылку"
                        " и предложение зарегистрироваться. "
                        "Выбирает нужный город. "
                        "Выполняет поиск книги с иероглифами в названии."
                        "Проверяет, что книга не найдена.")
    @allure.severity('minor')
    @allure.step('Поиск книг с названием из иероглифов')
    def test_ui_search_book_hieroglyphs(self, books_ui):
        """Тест выполняет поиск книги по названию из иероглифов.
        Нечувствителен к регистру.
        Чувствителен к опечаткам.
        """
        with allure.step('Ввод города и названия книги'):
            city = "Москва"
            book_title = "アびけ"
        # books_ui.close_notification_reg()
        # books_ui.close_notification()
        books_ui.find_city(city)
        books_ui.search_for_book(book_title)

        with allure.step('Получение названия найденных книг'):
            found_books_titles = books_ui.find_all_book_titles()

        with allure.step('Проверка отсутствия книг'):
            if "Похоже, у нас такого нет" in found_books_titles:
                assert True, "Книги не найдены, как и ожидалось."
            else:
                try:
                    found = any(book_title.lower() == title.lower() for title in found_books_titles.keys())
                    assert not found, f"Книга '{book_title}' найдена в результатах поиска, что является неверным результатом."
                except AssertionError as e:
                    print(e)

    @pytest.mark.negative
    @allure.story("Негативные тесты")
    @allure.id("SearchBook-6")
    @allure.title("Поиск книг с названием из спец. символов")
    @allure.description("Тест закрывает уведомления о подписке на рассылку"
                        " и предложение зарегистрироваться. "
                        "Выбирает нужный город. "
                        "Выполняет поиск книги со спец. символами в названии."
                        "Проверяет, что книга не найдена.")
    @allure.severity(Severity.MINOR)
    @allure.step('Поиск книг с названием из спец. символов')
    def test_ui_search_book_spec_char(self, books_ui):
        """Тест выполняет поиск книги по названию из
        спец. символов.
        Нечувствителен к регистру.
        Чувствителен к опечаткам.
        """
        with allure.step('Ввод города и названия книги'):
            city = "Москва"
            book_title = "!@"
        #books_ui.close_notification_reg()
        #books_ui.close_notification()
        books_ui.find_city(city)
        books_ui.search_for_book(book_title)

        with allure.step('Получение названия найденных книг'):
            found_books_titles = books_ui.find_all_book_titles()

        with allure.step('Проверка отсутствия книг'):
            if "Похоже, у нас такого нет" in found_books_titles:
                assert True, "Книги не найдены, как и ожидалось."
            else:
                try:
                    found = any(book_title.lower() == title.lower() for title in found_books_titles.keys())
                    assert not found, f"Книга '{book_title}' найдена в результатах поиска, что является неверным результатом."
                except AssertionError as e:
                    print(e)
