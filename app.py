"""
работа с библиотекой jinja2
jinja2 - очень удобное решение для отображения html страниц, это шаблонизатор, который позволяет передавать в текст
переменные, списки, словари и т.д., также в тексте можно прописывать логику pyhton: условия, циклы, макросы (которые
работают также как и функции в python) и т.д.
См. файл index.html

В jinja2 применяются фильтры (надстройки для рендеринга см. в index.html):
safe - безопасность по умолчанию, safe всегда отключен, он запрещает рендерить html теги на странице
lower,upper,capitalize - изменение строк (строчные буквы, заглавные буквы, первая буква большая)
trim - удалить лишние пробелы
striptags - удаляет все html теги у строки
----------------------------------------------------------------------
Это далеко не все фильтры, которые есть в jinja2, подробнее о фильтрах:
https://jinja.palletsprojects.com/en/2.10.x/

также jinja2 поддерживает такие функции как url_for() - это будет в дальнейших уроках.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    users_list = ['<b>Ivan</b>', '<b>Mike</b>', 'Peter', 'Vasiliy']  # передать список в jinga2
    user1 = {'name': 'ivan', 'age': 30, 'city': 'Moscow'}  # ivan передано с мал буквы, чтобы использ capitalize в index
    numbers = [10, 3, 4, 8, 1, 2]
    return render_template("index.html", title="Работа с jinja2",
                           users_list=users_list, user1=user1, numbers=numbers)


if __name__ == '__main__':
    app.run(debug=True)
