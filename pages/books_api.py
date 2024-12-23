import requests
import allure
from typing import Dict, List, Tuple, Any, Optional
from requests import Response

# Переменные для авторизации
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzUxMjE1OTYsImlhdCI6MTczNDk1MzU5NiwiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6IjhjN2UxYzZiZjExNTM4ZGQyNWRiOGI4ZTkxMWU4ZjJkZjVkODI2YjNkN2JmODg2OGIxYzNlNjNkMjkyNGMzZTIiLCJ0eXBlIjoxMH0.I5c5p6DAv2kP41AaMW-ROu-ouDFscvit4mZ7P2-nGDk"
MY_HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


class BooksApi:
    @allure.step(
        "Класс BooksApi содержит методы для работы с интернет-магазином \"Читай-город\""
    )
    def __init__(self, url: str) -> None:
        self.url = url
        self.my_headers = MY_HEADERS

    @allure.step("Api. Поиск книг по названию")
    def search_books(
        self, city_id: str = "213", value: str = ""
    ) -> Tuple[Dict[str, Any], int]:
        """Ищет книги по заданной фразе в указанном городе и возвращает ответ сервера в виде JSON и статус код."""
        with allure.step("Подготовка параметров запроса"):
            my_params = {"customerCityId": city_id, "phrase": value}
            response = requests.get(
                f"{self.url}/api/v2/search/product",
                headers=self.my_headers,
                params=my_params,
            )

        with allure.step("Обработка ответа"):
            response_json = response.json()
            with allure.step("Возврат результата"):
                return response_json, response.status_code

    def search_books_by_title(
        self, city_id: str = "213", title: str = "Нет текста для поиска"
    ) -> Tuple[Dict[str, Any], int]:
        """Ищет книги по заголовку и возвращает результат запроса и статус код."""
        return self.search_books(city_id=city_id, value=title)

    @allure.step("Api. Наличие книги в результатах поиска")
    def check_title_in_results(
        self, expected_title: str, resp_search: Dict[str, Any]
    ) -> List[str]:
        """Проверяет наличие заданного заголовка в результатах поиска и возвращает список найденных заголовков."""
        titles_included = []
        for book in resp_search.get("included", []):
            attributes = book.get("attributes", {})
            if "title" in attributes:
                titles_included.append(attributes["title"])
        return titles_included

    @allure.step("Api. Поиск книг по автору")
    def search_books_by_author(
        self, city_id: str, author_name: str
    ) -> Tuple[List[str], List[str], int, Dict[str, Any]]:
        """Ищет книги по имени автора и возвращает их названия и полные имена авторов."""
        resp_search, status_code = self.search_books(city_id=city_id, value=author_name)
        titles_included = []
        found_authors = []
        if status_code == 200:
            for book in resp_search.get("included", []):
                attributes = book.get("attributes", {})
                if "title" in attributes:
                    titles_included.append(attributes["title"])
                authors = attributes.get("authors", [])
                for author in authors:
                    full_name = f"{author['firstName']} {author['lastName']}"
                    found_authors.append(full_name)

        return titles_included, found_authors, status_code, resp_search

    @allure.step("Api. Подсчет книг у указанного автора")
    def count_books_by_author(
        self, resp_search: Dict[str, Any], author_first_name: str, author_last_name: str
    ) -> Tuple[int, List[str]]:
        """Считает количество книг у указанного автора и возвращает их количество с названиями."""
        book_count = 0
        titles_authors_included = []

        for book in resp_search.get("included", []):
            authors = book.get("attributes", {}).get("authors", [])
            for author in authors:
                if (author["firstName"] == author_first_name) and (
                    author["lastName"] == author_last_name
                ):
                    book_count += 1
                    titles_authors_included.append(
                        book.get("attributes", {}).get("title")
                    )

        return book_count, titles_authors_included

    @allure.step("Api. Добавление книг в корзину по ID")
    def add_books_to_cart(self, books: List[Dict[str, Any]]) -> List[int]:
        """Добавляет книги в корзину по их ID и возвращает список добавленных ID книг."""
        book_ids = []
        for book in books:
            attributes = book.get("attributes", {})
            status = attributes.get("status")

            if status == "canBuy":
                product_id = int(book["id"])
                book_ids.append(product_id)

        added_book_ids = []
        for product_id in book_ids:
            data = {
                "id": product_id,
                "adData": {"item_list_name": "search", "product_shelf": ""},
            }

            with allure.step("Отправка POST запроса для добавления книги в корзину"):
                response = requests.post(
                    f"{self.url}/api/v1/cart/product", headers=self.my_headers, json=data
                )
                try:
                    response_json = response.json()
                except requests.exceptions.JSONDecodeError:
                    response_json = {
                        "error": "Не удалось декодировать JSON",
                        "content": response.content.decode(),
                    }

                if response.status_code != 200:
                    raise Exception(
                        f"Книга с ID {product_id} не добавлена в корзину. Ответ: {response_json}"
                    )
                added_book_ids.append(product_id)

        return added_book_ids

    @allure.step("Api. Поиск информации о книге по id")
    def book_info(
        self, book_id: int, books_data: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Возвращает информацию о книге по ее идентификатору из предоставленного списка книг."""
        # Ищем книгу по ID в данных о книгах
        # print(f'Debug: Ищем книгу с ID: {book_id} в {len(books_data)} книгах.')
        book_data = next(
            (book for book in books_data if str(book["id"]) == str(book_id)), None
        )

        if book_data is None:
            print(f"Debug: Книга с ID {book_id} не найдена.")
        return book_data

    @allure.step("Api. Удаление всех книг из корзины")
    def delete_books_from_cart(self) -> Response:
        """Удаляет все книги из корзины и возвращает ответ сервера."""
        response = requests.delete(f"{self.url}/api/v1/cart", headers=self.my_headers)
        return response

    @allure.step("Api. Содержимое корзины")
    def get_cart_contents(self) -> Dict[str, Any]:
        """Возвращает содержимое корзины."""
        response = requests.get(f"{self.url}/api/v1/cart", headers=self.my_headers)
        return response.json()
