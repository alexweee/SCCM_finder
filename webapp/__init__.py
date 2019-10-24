from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.forms import LoginForm, ContactForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city
import sql_connector_01


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
#-----------------------------------------------------------
    @app.route('/')
    @login_required
    def index():
        title = "SCCM_finder"
        application_dropdown = ['Google Chrome', 'Kaspersky Antivirus']
        return render_template('index.html', page_title=title, dropdown=application_dropdown)

    @app.route('/proccess_search', methods=['GET', 'POST'])
    def proccess_search():
        user_select = request.form.get('dropdown')
        return redirect((f'/search/{user_select}'))

    @app.route('/search/<app_name>')
    def search_app(app_name: str):
        return(str(app_name))
        return sql_connector_01.sql_connection(str(app_name))

#-------------------------------------------------------------
    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Аутентификация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
        
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))
            if not user:
                flash('Неправильные имя пользователя')
                return redirect(url_for('login'))
            if not user.check_password(form.password.data):
                flash('Неправильный пароль')
                return redirect(url_for('login'))


    @app.route('/logout')
    def logout():
        logout_user()
        flash('ВЫ успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ!'
        else:
            return 'Ты не админ'

 #   @app.route('/test', methods=['GET'])
 #   def dropdown():
 #       colours = ['Google Chrome', 'Kaspersky Antivirus', 'Black', 'Orange']
 #       return render_template('test.html', colours=colours)

    return app
