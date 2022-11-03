
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from datetime import datetime, timedelta
import requests
import random
import string
import flask_restful
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
-m

@app.route("/")
def home():

    return render_template('base.html')

@app.context_processor
def utility_processor():
    def pluralize(count, singular, plural=None):
        if not isinstance(count, int):
            raise ValueError('"{}" must be an integer'.format(count))

        if plural is None:
            plural = singular + 's'

        string = singular if count == 1 else plural

        return "{} {}".format(count, string)

    return dict(pluralize=pluralize, now=datetime.now())


@app.route('/user')
def history():
    github = OAuth2Session(client_id, token=session['oauth_token'])
    username = str(github.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()['username'])
    historys = requests.get(BASE_USER + 'history', {'id': username}).json()
    return render_template('index_user.html', historys=historys)


@app.route('/user/generate_qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    if request.method == 'POST':
        buffer = BytesIO()
        data = request.form.get('data')

        img = qrcode.make(data)
        img.save(buffer)
        buffer.seek(0)
        response = send_file(buffer, mimetype='image/png', )
        return response
    else:
        github = OAuth2Session(client_id, token=session['oauth_token'])
        username = github.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()['username']
        result = requests.get(BASE_USER + 'User/' + str(username))
        expiration = datetime.now() + timedelta(0, 60)
        if result:
            result = requests.patch(BASE_USER + 'User/' + str(username), {"exp": expiration})
        else:
            result = requests.put(BASE_USER + 'User/' + str(username), {"exp": expiration})
        return render_template('qr_code.html', dat=result.json()['code'])


@app.route('/Scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        this_gate = {
            'id': request.json['id'],
            'secret': request.json['secret']
        }
        result = requests.get(BASE + 'Service/' + str(this_gate['id']))

        if str(result.json()['secret']) != str(this_gate['secret']):
            return '3'

        gate_history_resource_fields = {
            'id': this_gate['id'],
            'result': 'Denied',
            'date': str(datetime.now()),
        }
        code = "" + request.json['code']
        user = requests.put(BASE_USER + 'verify/' + str(code))
        if not user:
            requests.put(BASE + 'history', gate_history_resource_fields)
            return '0'
        user=user.json()
        valid = True
        if datetime.now() > parser.parse(user['exp']).replace(tzinfo=None):
            valid = False
        username = user['id']
        if valid:
            gate_history_resource_fields = {
                "id": this_gate['id'],
                "result": 'Allowed',
                "date": str(datetime.now()),
            }
            requests.put(BASE_USER + 'history',
                         {"id": username, "gate_id": int(this_gate['id']), "date": str(datetime.now()), })
            requests.patch(BASE + 'Service/' + str(this_gate['id']))
            requests.put(BASE + 'history', gate_history_resource_fields)
            return '1'
        else:
            requests.put(BASE + 'history', gate_history_resource_fields)
            return '2'
    else:
        return render_template('scanner.html')


@app.route('/Admin')
def index():
    gates = requests.get(BASE + 'Admin/').json()
    return render_template('index.html', gates=gates)


@app.route('/Admin/history')
def admin_history():
    historys = requests.get(BASE + 'history').json()
    return render_template('history_index.html', historys=historys)


@app.route('/Admin/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        id = request.form.get('id')
        location = request.form.get('location')
        secret = ''.join((random.choice(string.ascii_letters + '123456789') for i in range(10)))
        requests.put(BASE + 'Admin/', {"location": location, "secret": secret, "id": id})
        return redirect(url_for('index'))
    else:
        return render_template('add.html')


if __name__ != '__main__':


