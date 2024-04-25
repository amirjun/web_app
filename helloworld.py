
from flask import Flask, render_template

def index():
    
    return render_template('index.html') 

def second():
    return render_template('second.html')
app = Flask(__name__, template_folder = '', static_folder='')   

app.add_url_rule('/', 'index', index)  
app.add_url_rule('/second', 'second', second)
if __name__ == "__main__":
    
    app.run(debug=True) 
