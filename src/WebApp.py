import logging
from os import path

import Pyro4
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, SelectField, FileField

from utils import get_info, get_shared_folder, save_json

app = Flask(__name__, root_path="resources",
            static_folder="../resources/static",
            template_folder="../resources/templates")
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

socketio = SocketIO(app)

Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        option = int(form.language.data)
        main_uri = get_info()['containers']['MainController']['uri']
        obj = Pyro4.Proxy(main_uri)
        file = form.input_data.data
        file_path = path.join(get_shared_folder(), 'input.json')
        file.save(file_path)
        try:
            response = obj.run(action=option, input_json=file_path)
            print(response)
            response_path = save_json(response, path.join(get_shared_folder(), 'response.json'))
        except Exception as e:
            return render_template('index.html', form=form, message=str(e), async_mode=socketio.async_mode)
        return send_file(response_path,
                         attachment_filename="test.json", mimetype="text/json", as_attachment=True)

    return render_template('index.html', form=form, message=message, async_mode=socketio.async_mode)


@socketio.on('data')
def return_data():
    emit('data_response', get_info()['containers'])


class WebApp:
    def __init__(self):
        pass

    def start(self):
        socketio.run(app, host='0.0.0.0', port=9001, debug=False)


class NameForm(FlaskForm):
    language = SelectField(
        '¿Qué quieres hacer?',
        choices=[('1', 'Descargar Audio y Transcripciones'), ('2', 'Entrenar Modelos'), ('3', 'Speech2Text')]
    )
    input_data = FileField("Fichero de Entrada", validators=[FileRequired(), FileAllowed(['json'], 'Json only!')])
    submit = SubmitField('Submit')
