import pytest
import allure
from allure_commons.types import Severity
from pages.books_api import BooksApi

@allure.epic("API. Интернет-магазин Читай-город")
@allure.suite('API. Поиск книг в интернет-магазине "Читай-город"')
class TestBooksAPI:

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг")
    @allure.title("Тест: Поиск книги по части названия в Москве")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    @allure.step("1. Поиск книги по части названия в Москве с учетом регистра")
    def test_api_search_book_moscow(self, shopping_books):
        with allure.step('Ввод города и названия книги'):
            city_id = "213"
            title = "Гарри Поттер и Проклятое дитя."
        api = shopping_books

        with allure.step(
            f'Поиск книги с заголовком: "{title}" в городе с ID: {city_id}'
        ):
            resp_search, status_code = api.search_books_by_title(
                city_id=city_id, title=title
            )

        with allure.step("Статус-код = 200"):
            assert status_code == 200

        titles_included = api.check_title_in_results(title, resp_search)

        with allure.step("Вывод найденных книг"):
            print("Найденные книги:")
            for book in titles_included:
                print(f"- {book}")

        with allure.step("Сравнение искомой книги с найденными книгами"):
            assert any(title in book_title for book_title in titles_included)

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг")
    @allure.title("Тест: Поиск книги по полному названию в Санкт-Петербурге")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    @allure.step("2. Поиск книги по полному названию"
        " в Санкт-Петербурге без учета регистра")
    def test_api_search_book_other_city(self, shopping_books):
        api = shopping_books
        with allure.step("Передача параметров: город, название книги"):
            city_id = "2"
            title = "гарри поттер и философский камень"
            print(f"Ищу книги с заголовком: '{title}' в городе с ID: {city_id}")

        with allure.step("Выполнение поиска"):
            resp_search, status_code = api.search_books_by_title(
                city_id=city_id, title=title
            )

        with allure.step("Статус-код = 200"):
            assert status_code == 200

        titles_included = api.check_title_in_results(title, resp_search)

        with allure.step("Вывод найденных книг"):
            print("Найденные книги:")
            for book in titles_included:
                print(f"- {book}")

        with allure.step("Сравнение искомой книги с найденными книгами"):
            assert any(
                title.lower() in book_title.lower() for book_title in titles_included
            ), f'Искомое название: "{title}" не найдено в: {titles_included}'

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг. Позитивные тесты.")
    @allure.title("Тест: Поиск книги по автору в Минске")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.positive
    @allure.step("3. Поиск книги по автору в Минске")
    def test_api_search_book_author(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод города и автора'):
            city_id = "694357"
            author_first_name = "Джоан Кэтлин"
            author_last_name = "Роулинг"
            author_name = author_first_name + " " + author_last_name
        with allure.step(
            f'Поиск книги по автору: "{author_name}" в городе с ID: {city_id}'
        ):
            titles_included, found_authors, status_code, resp_search = (
                api.search_books_by_author(city_id=city_id, author_name=author_name)
            )
        with allure.step("Статус-код = 200"):
            assert status_code == 200
        with allure.step("Указанный автор присутствует в найденных книгах"):
            assert any(
                full_name.strip().lower() == author_name.lower()
                for full_name in found_authors
            ), f'Автор "{author_name}" не найден среди книг: {titles_included}. Найденные авторы: {found_authors}'
            book_count, titles_authors_included = api.count_books_by_author(
                resp_search=resp_search,
                author_first_name=author_first_name,
                author_last_name=author_last_name,
            )
        with allure.step("Вывод количества книг и названия"):
            print(f"Автор: {author_name}")
            print(f"Количество книг: {book_count}")
            print("Названия книг:")
            for title in titles_authors_included:
                print(f"- {title}")

    @allure.feature("API.Главная страница")
    @allure.story("Добавление книг в корзину")
    @allure.title("Тест: Добавление книг в корзину")
    @allure.severity(Severity.BLOCKER)
    @pytest.mark.positive
    @allure.step("4. Добавление найденных книг в корзину")
    def test_api_add_books_to_cart(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод названия книги'):
            book_title = "Белоснежка и семь гномов"

        with allure.step(f'Поиск книги по заголовку: "{book_title}"'):
            resp_search, status_code = api.search_books_by_title(title=book_title)

        with allure.step("Статус-код = 200"):
            assert status_code == 200, f"Ожидался статус код 200, получен {status_code}"

        with allure.step("Добавление найденных книг в корзину"):
            added_books = api.add_books_to_cart(resp_search.get("included", []))

        with allure.step("Проверка, что книги добавлены в корзину"):
            assert added_books, "Не найдено доступных книг для добавления в корзину."

        with allure.step("Вывод информации о добавленных книгах в корзину"):
            print(f"В корзину добавлено {len(added_books)} книг:")
            for book_id in added_books:
                book_data = api.book_info(
                    book_id, resp_search.get("included", [])
                )  # Получаем данные о книге по ID

                # Проверяем, получаем ли мы title корректно
                if book_data:
                    title = book_data.get("attributes", {}).get("title")
                else:
                    title = "Нет названия"

                print(f"ID: {book_id}, Название: {title}")

        with allure.step("Очистка корзины после добавления книг"):
            response = api.delete_books_from_cart()
            assert (
                response.status_code == 204
            ), f"Ожидался статус 204, но получен {response.status_code}."

    @allure.feature("API. Корзина")
    @allure.story("Удаление книг из корзины")
    @allure.title("Тест: Удаление книг из корзины")
    @allure.severity(Severity.BLOCKER)
    @allure.step("5. Удаление всех книг из корзины")
    @pytest.mark.positive
    def test_api_delete_books_cart(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод города и названия книги'):
            city_id = "213"
            title = "Белоснежка и семь гномов"
        with allure.step(
            f'Поиск книги с заголовком: "{title}" для добавления в корзину'
        ):
            resp_search, status_code = api.search_books_by_title(
                city_id=city_id, title=title
            )
            assert (
                status_code == 200
            ), f"Ошибочный статус код {status_code} при поиске книги"

        with allure.step("Добавление найденной книги в корзину"):
            added_book_ids = api.add_books_to_cart(resp_search.get("included", []))
            assert added_book_ids, "Не удалось добавить книги в корзину"
        with allure.step("Удаление книг из корзины"):
            response = api.delete_books_from_cart()
            with allure.step("Статус-код = 204"):
                assert (
                    response.status_code == 204
                ), f"Ожидался статус 204, но получен {response.status_code}"

            cart_contents = api.get_cart_contents()
            with allure.step("Книг нет в корзине"):
                assert (
                    cart_contents.get("products", []) == []
                ), "Ожидалась пустая корзина, но она содержит товары."

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг. Негативные тесты.")
    @allure.title("Тест: Поиск книги с названием из одного символа")
    @allure.severity(Severity.BLOCKER)
    @allure.step("6. Поиск книг с названием из одного символа")
    @pytest.mark.negative
    def test_api_search_books_invalid_phrase(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод названия книги'):
            phrase = "p"
        response_json, status_code = api.search_books(value=phrase)

        with allure.step("Статус-код = 400"):
            assert status_code == 400, f"Ожидался статус 400, получен {status_code}"

        with allure.step("Наличие ошибок в ответе"):
            assert "errors" in response_json, 'Ответ не содержит ключ "errors"'
            assert len(response_json["errors"]) > 0, "Список ошибок пуст"

        with allure.step(
            "Наличие ожидаемого сообщения об ошибке"
        ):
            error_message = response_json["errors"][0]["title"]
            expected_error_message = "Phrase должен содержать минимум 2 символа"
            assert error_message == expected_error_message, (
                f'Ожидалось сообщение об ошибке "{expected_error_message}", '
                f'получено "{error_message}"'
            )
            print(f'Получено сообщение об ошибке: "{error_message}"')

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг")
    @allure.title("Тест. Поиск книги с неправильным регистром")
    @allure.severity(Severity.NORMAL)
    @allure.step("7. Поиск книги с неправильным регистром")
    @pytest.mark.negative
    def test_api_search_book_sensitive_register(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод города и названия книги'):
            city_id = "213"
            title = "гарри поттер и проклятое дитя."

        with allure.step(
            f'Поиск книги с заголовком: "{title}" в городе с ID: {city_id}'
        ):
            resp_search, status_code = api.search_books_by_title(
                city_id=city_id, title=title
            )

        with allure.step("Статус-код = 200"):
            assert status_code == 200

        titles_included = api.check_title_in_results(title, resp_search)

        with allure.step("Проверка отсутствия искомой книги с учетом регистра"):
            if any(title == book_title for book_title in titles_included):
                message = (
                    f'Книга с названием "{title}" найдена, но регистр указан неверно.'
                )
                print(message)
                assert False, message
            else:
                print(
                    f'Книга с названием "{title}" не найдена, причина: несоблюдение регистра.'
                )

        with allure.step("Вывод найденных книг"):
            print("Найдены похожие книги:")
            for book in titles_included:
                print(f"- {book}")

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг")
    @allure.title("Тест: Поиск книги с названием из иероглифов")
    @allure.severity(Severity.MINOR)
    @allure.step("8. Поиск книг с названием из иероглифов")
    @pytest.mark.negative
    def test_api_search_books_hieroglyphs(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод названия книги'):
            phrase = "アびけ"
        response_json, status_code = api.search_books(value=phrase)

        with allure.step("Статус-код = 422"):
            assert status_code == 422, f"Ожидался статус 400, получен {status_code}"

        with allure.step("Наличие ошибок в ответе"):
            assert "errors" in response_json, 'Ответ не содержит ключ "errors"'
            assert len(response_json["errors"]) > 0, "Список ошибок пуст"

        with allure.step(
            "Наличие ожидаемого сообщения об ошибке"
        ):
            error_message = response_json["errors"][0]["title"]
            expected_error_message = "Недопустимая поисковая фраза"
            assert error_message == expected_error_message, (
                f'Ожидалось сообщение об ошибке "{expected_error_message}", '
                f'получено "{error_message}"'
            )
            print(f'Получено сообщение об ошибке: "{error_message}"')

    @allure.feature("API.Главная страница")
    @allure.story("Поиск книг")
    @allure.title("Тест: Поиск книги с названием из спец.символов")
    @allure.severity(Severity.MINOR)
    @allure.step("9. Поиск книг с названием из спец.символов")
    @pytest.mark.negative
    def test_api_search_books_spec_char(self, shopping_books):
        api = shopping_books
        with allure.step('Ввод названия книги'):
            phrase = "!@"
        response_json, status_code = api.search_books(value=phrase)

        with allure.step("Статус-код = 422"):
            assert status_code == 422, f"Ожидался статус 400, получен {status_code}"

        with allure.step("Наличие ошибок в ответе"):
            assert "errors" in response_json, 'Ответ не содержит ключ "errors"'
            assert len(response_json["errors"]) > 0, "Список ошибок пуст"

        with allure.step(
            "Наличие ожидаемого сообщения об ошибке"
        ):
            error_message = response_json["errors"][0]["title"]
            expected_error_message = "Недопустимая поисковая фраза"
            assert error_message == expected_error_message, (
                f'Ожидалось сообщение об ошибке "{expected_error_message}", '
                f'получено "{error_message}"'
            )
            print(f'Получено сообщение об ошибке: "{error_message}"')

    if __name__ == "__main__":
        pytest.main()
