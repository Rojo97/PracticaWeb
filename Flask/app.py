from os import environ
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
#from models import db, Chat

load_dotenv(find_dotenv())
app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
if environ.get('DEBUG') == 'True':
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False
app.config['PORT'] = 80

# Socketio
DOMAIN = environ.get('DOMAIN')
socketio = SocketIO(app)

'''# Database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE')
db.init_app(app)'''


@app.route('/groups')
def groups_template():
    groups = [
      { "id": 1, "name": "Todos", "num": 26, "class": "fa-calendar-minus-o"},
      { "id": 2, "name": "Salón", "num": 5, "class": "fa-home"},
      { "id": 3, "name": "Cocina", "num": 3, "class": "fa-home"},
      { "id": 4, "name": "Pasillo", "num": 2, "class": "fa-home"},
      { "id": 5, "name": "Luces", "num": 14, "class": "fa-lightbulb-o"}
    ]
    return render_template(
        'index.html',
        domain=DOMAIN,
        groups=groups
    )
@app.route('/newGroup')
def new_groups_template():
    return render_template(
        'new-group.html',
        domain=DOMAIN
    )
@app.route('/')
def login_template():
    return render_template(
        'login2.html',
        domain=DOMAIN
    )
@app.route('/register')
def register_template():
    return render_template(
        'registro2.html',
        domain=DOMAIN
    )
@app.route('/recoverPass')
def recover_password_template():
    return render_template(
        'recuperarPassword.html',
        domain=DOMAIN
    )

@app.route('/newSensor')
def new_sensor_template():
    return render_template(
        'addSensor.html',
        domain=DOMAIN
    )

@app.route('/addToGroup')
def add_to_group_template():
    return render_template(
        'addToGroup.html',
        domain=DOMAIN
    )

@app.route('/changePass')
def change_pass_template():
    return render_template(
        'cambiarPassword.html',
        domain=DOMAIN
    )

@app.route('/manageUserGroups')
def manage_user_groups_template():
    return render_template(
        'gestionarUsuariosGrupos.html',
        domain=DOMAIN
    )

@app.route('/group')
def group_template():
    return render_template(
        'grupos.html',
        domain=DOMAIN
    )

@app.route('/newData')
def new_data_template():
    return render_template(
        'introducirDatos.html',
        domain=DOMAIN
    )
@app.route('/newProgram')
def new_program_template():
    return render_template(
        'newProgram.html',
        domain=DOMAIN
    )
@app.route('/programs')
def programs_template():
    programs = [
      { "id": 1, "group": "Cochera", "name": "Luces de la cochera", "class": "fa-clock-o"},
      { "id": 2, "group": "Salón", "name": "Luces del salon", "class": "fa-clock-o"},
      { "id": 3, "group": "Salón", "name": "Temperatura del salon", "class": "fa-clock-o"},
      { "id": 4, "group": "Cocina", "name": "Luces de la cocina", "class": "fa-clock-o"},
      { "id": 5, "group": "Cocina", "name": "Temperatura de la cocina", "class": "fa-clock-o"},
    ]
    return render_template(
        'programas.html',
        domain=DOMAIN,
        programs=programs
    )
@socketio.on('createGroup')
def greateGroup(group):
    # Send message to alls users
    print(group)


if __name__ == '__main__':
    socketio.run(app)
