from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
# так делать запрещено! ключ должен быть скрыт, например в перемен текущ терминальн сессии
# но для упрощения учебного примера здесь сделан простой ключ, но в реальном проекте он сложный и скрыт
app.config['SECRET_KEY'] = "test###"


@app.route('/')
def index():
    return render_template('index.html')


class NameForm(FlaskForm):
    """в этом классе создаются формы и задаётся валидация этих форм
    они будут проброшены в flask для дальнейшей работы с ними"""
    name = StringField("Как Вас зовут?", validators=[DataRequired()])  # здесь будет выполн проверка на пустоту
    password = PasswordField("Ваш пароль", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/name', methods=['GET', 'POST'])
def name():
    """обработка введенных данных в форму"""
    name_field = None
    psw_field = None
    form = NameForm()
    if form.validate_on_submit():  # если форма прошла валидацию, то записать переменные и показать приветствие
        name_field = form.name.data
        psw_field = form.password.data
        form.name.data = ''
        flash("Успешно, всё получилось!")  # отправка flash сообщения (также у сообщений ещё есть параметр category)
    return render_template('name.html', name=name_field, psw=psw_field, form=form)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error)


if __name__ == '__main__':
    app.run(debug=True)
