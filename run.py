from config import Configuration
from flask import Flask, render_template, request, redirect, url_for, flash
from loguru import logger
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Configuration)  # загрузка конфигурации из класса с конфигурацией
db = SQLAlchemy(app)
"""
Удобность миграции в том, что все взаимодействия с БД выполняются под капотом, то есть не нужно удалять таблицы и прочие
танцы с бубном, всё делается автоматом, при условии, что в приложении создан экземпляр класса Migrate(), в нём 
связываются базы данных и приложение.
------------------------------------------------------------------------------------------------------
За тем в bash консоли нужно сделать следующее:
export FLASK_ENV=development    -указать что приложение запущено в рамках режима разработки
export FLASK_APP=run.py     -указать на файл который отвечает за приложение
flask db init       -по аналогии с github, будет создана папка, контролирующая версии базы данных
flask db migrate -m 'Initial Migrate'   -создание слепка текущей базы данных
flask db upgrade    -обновление таблицы
--------------------------------------------------------------------------------------------
О том, что всё прошло успешно, будет говорить тот факт, что создалась папка migrations
--------------------------------------------------------------------------------------------
"""
migrate = Migrate(app, db)


# модель класс Users нужно будет перенести в отдельный файл (но при этом нужно решить проблему с цикличным импртом)
class Users(db.Model):
    """класс модель пользователя (определение данных которые будут хранится в sql)"""
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    favorite_color = db.Column(db.String(100))
    data_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Name: {db.name} email: {db.email}>"


class FormAddUser(FlaskForm):
    """форма которая будет отправлена пользователю"""
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template('index.html', title="Главная страница")


@app.route('/test_slot1')
def slot1():
    user = Users(name="Ivan", email="iv@yandex.ru")
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/user/show')
def user_show():
    all_users = Users.query.order_by(Users.data_added)  # выгрузить всех пользователей в порядке добавления
    return render_template("users_show.html", users=all_users)


@app.route('/user/add', methods=['POST', 'GET'])
def user_add():
    noform = False
    form = FormAddUser()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
            flash('Пользователь успешно добавлен', category='succes')
            noform = True
        else:
            flash('Не добавлено. Пользователь с таким email уже существует. Попробуйте ещё раз...', category='error')
        form.name.data = None
        form.email.data = None
        form.favorite_color.data = None
    return render_template('user_add.html', form=form, noform=noform)


@app.route('/update/<int:user_id>', methods=['POST', 'GET'])
def update(user_id):
    noform = False
    form = FormAddUser()  # для формы обновления данных можно использ тy же форму, что и для добавления пользователя
    # в строке ниже считываются данные о пользователе из БД
    name_to_update = Users.query.get_or_404(user_id)  # если пользователь с таким Id не существует то 404
    if request.method == 'POST':
        # в строчках ниже происходит обновление данных в модели
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()  # если всё корректно, то подтвердить изменения в БД
            flash('Данные успешно обновлены', category='succes')
            noform = True
            return render_template('update.html', form=form, name_to_update=name_to_update,
                                   noform=noform)
        except Exception as err:
            logger.error(err)  # логировать исключение
            flash('Проблема, данные не были обновлены', category='succes')
            return render_template('update.html', form=form, name_to_update=name_to_update,
                                   noform=noform)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update,
                               noform=noform)


@app.route('/delete/<int:user_id>')
def user_delete(user_id):
    user_to_delete = Users.query.get_or_404(user_id)
    form = FormAddUser()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Пользователь удалён.', category='succes')
        return render_template("update.html", noform=True)
    except Exception as err:
        logger.error(err)
        flash("Этого пользователя удалить нельзя", category="error")
        return render_template("update.html", noform=False, form=form)


@app.errorhandler(404)
def error_application(error):
    logger.error(error)  # логирование
    msg = "Ошибка 404, такой страницы не существует"
    return render_template("error.html", msg=msg)


#
# @app.errorhandler(Exception)
# def error_unknuw(error):
#     logger.error(error)  # логирование
#     msg = "Неизвестная ошибка, попробуйте ещё"
#     return render_template("error.html", msg=msg)


if __name__ == '__main__':
    app.run()
