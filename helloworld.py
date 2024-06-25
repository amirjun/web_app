# импортирование ресурсов 
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# создание веб-приложений и его базы данных
###  template_folder и static_folder- папки для веб-страниц и стилей
### если эти папки='', то это значит, что в качестве этих папок используется папка проекта              
app = Flask(__name__, template_folder = '', static_folder='')   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
database = SQLAlchemy(app)
# переменные веб-приложения
locked_status = True

# создание таблицы в базе данных
### создание класса Пользователь имеющего такие данные:
### -> номер, email, пароль, имя, возраст, город
### у каждого свойства пользователя прописан тип данных
### -Ю и дополнительные атрибуты, если они есть
class User(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    ### может быть только 1 пользователь с таким email(unique=True)
    email = database.Column(database.String(100), unique=True)
    password = database.Column(database.String(100))
    name = database.Column(database.String(100))
    age = database.Column(database.Integer)
    city = database.Column(database.String(100))

    #   notes = database.relationship('Note', backref=database.backref('user', lazy=True))
### этот класс находится в процессе разработки
class Note(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    title = database.Column(database.String(100))
    text = database.Column(database.String(1000))
# экземпляр эксперементального класса
note1 = Note(title = 'о комариках', text = 'комарики классные, но пчелки лучше')

# фунция, обслуживающая корень сайта(главную страницу) 
def index():
    ### показывание HTML-шаблона
    global locked_status
    context ={
        'status':not (locked_status)
    }
    

    return render_template('index.html', context=context)
 
# фунция, обслуживающая закрытую страницу
@app.route('/second', methods=('GET', 'POST'))
def second():
    ### объявление глобальной переменной 
    global locked_status 
    ### если страница заблокирована, переносимся на страницу логина
    if locked_status == True:
        return redirect('/login')
    
    if request.method == 'POST':
        if request.form['Submit'] =='Сохранить':
            post_name = request.form['post-name']
            post_text = request.form['post-text']
            note=Note(title=post_name, text=post_text)
            try:
                database.session.add(note)
                database.session.commit()
            except:
                database.session.rollback()
                print('Ошибка записи в бд')
        else:
            post_id = request.form['post-id'] 
            note = Note.query.get(post_id)
            if note:
                database.session.delete(note)
            database.session.commit()
            print('Заметка удалена')

    context = {
        'posts': Note.query.all()
    }

    ### показывание заблокированной страницы
    return render_template('second.html', context=context)
# фунция, обслуживающая страницу регистрации
@app.route('/registr', methods=('GET', 'POST'))
def registr():
    ### проверка на то, что форма передает данные о пользователе
    if request.method == 'POST':
        ### запрос данных у пользователя
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        ### создание нового пользователя по полученным данным
        user = User(
            email = email, password = password, name = name, age = age, city=city
        )
        print('Данные пользователя собраны!')
        ### добавление нового пользователя в базу данных
        try:
            database.session.add(user)
            database.session.commit()
        except:
            database.session.rollback()
            print('Ошибка записи в бд')

    return render_template('registr.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            global locked_status
            locked_status = False
            return redirect('/second')
    return render_template('login.html')
# база данных создается тогда и только тогда, когда работает приложение     
with app.app_context():
    database.create_all()
# привязка веб-адресов проекта к функциям(маршрутизация)
app.add_url_rule('/', 'index', index)  
app.add_url_rule('/second', 'second', second)
app.add_url_rule('/registr', 'registr', registr)
app.add_url_rule('/login', 'login', login)
# запуск веб-приложений в одном процессе
if __name__ == "__main__":  
    
    app.run(debug=True)

