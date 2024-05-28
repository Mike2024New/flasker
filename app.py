"""
также приложение можно запустить из консоли linux ->
1. создать переменные:
export FLASK_ENV=development     - выбор среды конфигураций
export FLASK_APP=app.py     -указать файл в котором приложение flask
flask run       - запуск приложения
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    return f"Добро пожаловать, {name}!"


if __name__ == '__main__':
    app.run(debug=True)
