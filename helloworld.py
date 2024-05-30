
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy             
app = Flask(__name__, template_folder = '', static_folder='')   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
database = SQLAlchemy(app)

locked_status = True

class User(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    email = database.Column(database.String(100), unique=True)
    password = database.Column(database.String(100))
    name = database.Column(database.String(100))
    age = database.Column(database.Integer)
    city = database.Column(database.String(100))

    notes = database.relationship('Note', backref=database.backref('user', lazy=True))

class Note(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    title = database.Column(database.String(100))
    text = database.Column(database.String(1000))

note1 = Note(title = 'о комариках', text = 'комарики классные, но пчелки лучше')


def index():
    return render_template('index.html')
 

def second():
    global locked_status 
    if locked_status == True:
        return redirect('/login')
    return render_template('second.html')

@app.route('/registr', methods=('GET', 'POST'))
def registr():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        user = User(
            email = email, password = password, name = name, age = age, city=city
        )
        print('Данные пользователя собраны!')
        try:
            database.session.add(user)
            database.session.commit()
        except:
            database.session.rollback()
            print('Ошибка записи в бз')

    return render_template('registr.html')
with app.app_context():
    database.create_all()

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
    

app.add_url_rule('/', 'index', index)  
app.add_url_rule('/second', 'second', second)
app.add_url_rule('/registr', 'registr', registr)
app.add_url_rule('/login', 'login', login)

if __name__ == "__main__":  
    
    app.run(debug=True)

