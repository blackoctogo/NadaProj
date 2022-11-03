
from flask import *


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/contribuer")
def contribute():
    return render_template('contribute.html')

@app.route("/mentions-legales")
def ml():
    return render_template('ml.html')

if __name__ == '__main__':
    app.run(debug=True)
