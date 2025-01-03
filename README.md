# pytest_ui_api_template

## Автоматизации тестирования на python, проект "Читай-город"

### Шаги
Список команд для работы с проектом:
1. Склонировать проект с помощью команды: ```git clone https://github.com/VikaSkypro/Vika.I_Diploma.git```
2. Установить зависимости: ```pip install > -r requirements.txt```
3. Запустить тесты: ```pytest -s -v```
4. Сгенерировать отчет: ```allure generate allure-result -o allure-report```
5. Открыть отчет: ```allure open allure-report```

### Стек:
- pytest
- selenium
- requests
- allure
- json

### Струткура:
- ./test - тесты 
- ./pages - описание страниц

### Библиотеки
- pyp install pytest
- pip install selenium
- pip install webdriver-manager
- pip install allure-pytest
- pip install requests
- pip install fuzzywuzzy

### Запуск тестов
Запуск тестов UI проходит без авторизации.
Запуск тестов API __требует авторизации__. Для этого необходимо:
1. Перейти по ссылке https://www.chitai-gorod.ru/ на сайт Читай-город
2. Пройти авторизацию, используя доступный номер телефона.
3. Нажать F12 (или правой кнопкой мыши на любом элементе и выбрать пункт "Посмотреть код")
4. Перейти на вкладку Application - Storage -> Cookies -> https://www.chitai-gorod.ru
5. В таблице найти поле Name: access-token и скопировать из Value TOKEN без приставки "Bearer%20"
6. Скопированный TOKEN вставить в файл BooksApi.py в переменную TOKEN = ""
7. запускать тесты.

### Отчет
По результатам проведения тестов сформирован отчет в Allure. Отчет хранится в директории _allure_report_all_.
Его можно запустить из VSCode или PyCharm командой:
```
allure open allure-report
```

### Инструкция по запуску тестов для формирования отчета Allure
1. Перейти в директорию с тестами.
2. Запустить тесты и указать путь к каталогу результатов тестирования:
   ```
   pytest --alluredir allure-result
   ```
   или
   ```
   python -m pytest --alluredir allure-result
   ```
   В директории с тестами появится папка ***allure-result***. Там сохранятся отчеты о тестах.
3. Следующая команда запускает Allure и конвертирует результаты теста в отчет:
   ```
   allure serve allure-result
   ```
   
4. В командной строке нажать ```Ctrl+C -> Y``` - это завершает работу утилиты.
5. _Allure Report_ — это утилита. Она обрабатывает результаты тестирования и создает HTML-отчет.
   Allure умеет генерировать отчет в файл — его можно выгружать. 

   Для этого используется команда:
   ```
   allure generate allure-result 
   ```
   где, allure-result это название папки.

   Результат выгрузится в папку ***allure-report***.
6. В файле __index.html__ хранится результат отчета, его можно запускать с помощью команды:
   ```
   allure open allure-report
   ```
   Если вы отправите папку allure-report коллеге, то он сможет открывать этой командой результаты у себя на компьютере.

### Ссылка на проект:
[Ссылка на проект "Читай-город"](https://vikaskypro.yonote.ru/share/9c5eaf76-514d-45aa-bf1c-e2c26514abc6)