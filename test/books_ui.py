import pytest
import allure
from allure_commons.types import Severity
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
from fuzzywuzzy import fuzz

class BooksIU:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Api. Выбор города")
    # def find_city(self, city) -> None:
    #     """ Метод работает с popup выбора города.
    #      Если город совпадает с нужным -
    #      закрывает popup. Если нет -
    #      происходит выбор нужного города
    #      """
    #     try:
    #         with allure.step('Ожидание появления popup для изменения города'):
    #             city_popup = WebDriverWait(self.driver, 10).until(
    #                 EC.visibility_of_element_located(
    #                     (By.CSS_SELECTOR, ".change-city.change-city-container__popup-confirmation"))
    #             )
    #
    #         with allure.step('Есть popup'):
    #             if city_popup:
    #                 with allure.step('Указан нужный город'):
    #                     city_title = city_popup.find_element(By.CSS_SELECTOR, ".change-city__title").text
    #                 if city in city_title:
    #                     with allure.step('Город совпадает, нажимаем кнопку "Да, я здесь"'):
    #                         button_yes = city_popup.find_element(By.CSS_SELECTOR,
    #                                                              ".button.change-city__button.change-city__button--accept.blue")
    #                         button_yes.click()
    #
    #                     with allure.step('Popup закрылся'):
    #                         WebDriverWait(self.driver, 10).until(
    #                             EC.invisibility_of_element(city_popup)
    #                         )
    #                 else:
    #                     with allure.step('Город не совпадает, нажимаем кнопку "Нет, изменить город"'):
    #                         button_no = city_popup.find_element(By.CSS_SELECTOR,
    #                                                             ".button.change-city__button.change-city__button--cancel.light-blue")
    #                         button_no.click()
    #
    #                     with allure.step('Ожидание появления popup для выбора города'):
    #                         city_modal = WebDriverWait(self.driver, 10).until(
    #                             EC.visibility_of_element_located((By.CSS_SELECTOR, ".city-modal__content"))
    #                         )
    #
    #                     with allure.step('Поиск и выбор нужного города'):
    #                         city_option = city_modal.find_element(By.XPATH, f"//li[contains(text(), '{city}')]")
    #                         city_option.click()
    #
    #                     with allure.step('Popup закрылся'):
    #                         WebDriverWait(self.driver, 10).until(
    #                             EC.invisibility_of_element(city_modal)
    #                         )
    #     except Exception as e:
    #         print(f"Произошла ошибка при работе со всплывающим окном: {e}")
    #


    @allure.step("Api. Выбор города")
    def find_city(self, city) -> None:
        """ Метод работает с popup выбора города.
        Если город совпадает с нужным -
        закрывает popup. Если нет -
        происходит выбор нужного города.
        """
        try:
            with allure.step('Ожидание появления popup для изменения города'):
                city_popup = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, ".change-city.change-city-container__popup-confirmation"))
                )
            self.handle_city_popup(city_popup, city)

        except TimeoutException:
            with allure.step('Попап не найден, проверяем текущий город'):
                current_city_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, ".header-city__title"))
                )
                current_city = current_city_element.text

                if city in current_city:
                    with allure.step('Текущий город совпадает, завершаем метод'):
                        return
                else:
                    with allure.step('Текущий город не совпадает, меняем город'):
                        current_city_element.click()
                    # Ожидаем появления модала выбора города
                    city_popup = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, ".change-city.change-city-container__popup-confirmation"))
                    )
                    self.handle_city_popup(city_popup, city)

    def handle_city_popup(self, city_popup, city):
        """ Обрабатывает попап выбора города. """
        with allure.step('Обработка pop-up для выбора города'):
            city_title = city_popup.find_element(By.CSS_SELECTOR, ".change-city__title").text
            if city in city_title:
                with allure.step('Город совпадает, нажимаем кнопку "Да, я здесь"'):
                    button_yes = city_popup.find_element(By.CSS_SELECTOR,
                                                         ".button.change-city__button.change-city__button--accept.blue")
                    button_yes.click()

                with allure.step('Popup закрылся'):
                    WebDriverWait(self.driver, 10).until(
                        EC.invisibility_of_element(city_popup)
                    )
            else:
                with allure.step('Город не совпадает, нажимаем кнопку "Нет, изменить город"'):
                    button_no = city_popup.find_element(By.CSS_SELECTOR,
                                                        ".button.change-city__button.change-city__button--cancel.light-blue")
                    button_no.click()

                with allure.step('Ожидание появления popup для выбора города'):
                    city_modal = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".city-modal__content"))
                    )

                with allure.step('Поиск и выбор нужного города'):
                    city_option = city_modal.find_element(By.XPATH, f"//li[contains(text(), '{city}')]")
                    city_option.click()

                with allure.step('Popup закрылся'):
                    WebDriverWait(self.driver, 10).until(
                        EC.invisibility_of_element(city_modal)
                    )

    def close_notification_reg(self):
        """Метод закрывает предложение авторизации и скидки"""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "popmechanic-main"))
            )
            close_button = self.driver.find_element(By.CLASS_NAME, "popmechanic-close")
            close_button.click()
        except TimeoutException:
            pass

    @allure.step("Api. Закрытие уведомления о подписке")
    def close_notification(self) -> None:
        """Метод закрывает уведомление о подписке"""
        try:
            notification = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.push-notification__balloon"))
            )
            close_button1 = notification.find_element(By.CSS_SELECTOR, "button.push-notification__no-button")
            close_button1.click()
        except TimeoutException:
            pass

    @allure.step("Api. Поиск книг по названию")
    def search_for_book(self, book_title) -> None:
        """Метод находит поле поиска, вводит фразу и нажимает Enter."""
        try:
            with allure.step('Ожидание появления поля поиска'):
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="phrase"]'))
                )

            with allure.step('Ввод фразы в поле поиска'):
                search_input.clear()
                search_input.send_keys(book_title)
                search_input.send_keys(Keys.RETURN)

        except TimeoutException:
            print("Поле поиска не появилось в течение заданного времени.")
        except NoSuchElementException:
            print("Поле поиска не найдено.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        pass

    @allure.step("Api. Сбор названий книг в словарь")
    def find_all_book_titles(self) -> dict:
        """
        Метод для поиска всех названий книг
        и возврата их в виде словаря.
        Ключи - названия книг (строки),
        значения - индексы (например, 1, 2, 3).
        Если книг нет, возвращает сообщение.
        """
        book_titles = {}
        no_books_message = "Похоже, у нас такого нет"

        with allure.step("Поиск всех книг в контейнере"):
            attempts = 1  # Количество попыток поиска
            for attempt in range(attempts):
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//article[@class='product-card product-card product']"))
                    )

                    with allure.step("Получаем общее количество статей (книг)"):
                        articles = self.driver.find_elements(By.XPATH,
                                                             "//article[@class='product-card product-card product']")
                        articles_count = len(articles)

                        if articles_count == 0:
                            no_books_element = self.driver.find_elements(By.XPATH,
                                                                         "//h4[contains(text(),'Похоже, у нас такого нет')]")
                            if no_books_element:
                                return {no_books_message: []}

                        for index, article in enumerate(articles, start=1):
                            try:
                                title_element = article.find_element(By.XPATH, ".//div[2]/a[1]/div[1]/div[1]")
                                title = title_element.text.strip()

                                if title:
                                    if title not in book_titles:
                                        book_titles[title] = []

                                    book_titles[title].append(index)

                                    with allure.step(f"1.{index} Найдено название книги: {title}"):
                                        continue

                            except NoSuchElementException:
                                with allure.step(f"1.{index} Название книги не найдено в статье {index}"):
                                    continue
                            except StaleElementReferenceException:
                                with allure.step(f"1.{index} Ошибка! Ссылка на элемент устарела в статье {index}"):
                                    break

                    with allure.step("Проверка, все ли книги найдены"):
                        if len(book_titles) >= articles_count:
                            break

                except TimeoutException:
                    with allure.step(f"Ошибка: Время ожидания истекло при попытке {attempt + 1}. Книги не загружены."):
                        continue
                except Exception as e:
                    with allure.step(f"Ошибка во время попытки {attempt + 1}: {str(e)}"):
                        continue

        return book_titles
