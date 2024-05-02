
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder = '', static_folder='')   
def index():
    return render_template('index.html') 

def second():
    return render_template('second.html')

@app.route('/registr', methods=('GET', 'POST'))
def registr():
    return render_template('registr.html')

app.add_url_rule('/', 'index', index)  
app.add_url_rule('/second', 'second', second)
if __name__ == "__main__":
    
    app.run(debug=True)
