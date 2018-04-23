from os import environ
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import models

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

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE')
db.init_app(app)

@app.route('/groups')
def groups_template():
    groups = []
    allgroups = models.Grupo.query(all)
    for n in allgroups:
        groups.append({"id": n.grupoID, "name": n.nombre, "num": len(n.sensores), "class": n.clase})
    return render_template(
        'index.html',
        domain=DOMAIN,
        groups=groups
    )
@app.route('/newGroup')
def new_groups_template():
    devices = [
      { "id": 1, "group": "Cochera", "name": "Luces de la cochera", "type": "light"},
      { "id": 2, "group": "Salón", "name": "Luces del salon", "type": "light"},
      { "id": 3, "group": "Salón", "name": "Temperatura del salon", "type": "thermostat"},
      { "id": 4, "group": "Cocina", "name": "Luces de la cocina", "type": "light"},
      { "id": 5, "group": "Cocina", "name": "Temperatura de la cocina", "type": "thermostat"},
    ]
    return render_template(
        'new-group.html',
        domain=DOMAIN,
        devices=devices
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
    actuadores = []
    allactuadores = models.Dispositivo.query(all).filter_by(tipo = "actuador")
    for n in allactuadores:
        actuadores.append({"id": n.disID, "name": n.nombre , "Estado": n.estado, "class": n.clase})
    return render_template(
        'newProgram.html',
        domain=DOMAIN, actuadores = actuadores
    )
@app.route('/programs')
def programs_template():
    programs = []
    allprograms = models.ProgramaGrupo.query(all)
    for n in allprograms:
        programs.append({ "id": n.progID, "group": n.grupo.nombre, "name": n.nombre, "class": "fa-clock-o"})
    return render_template(
        'programas.html',
        domain=DOMAIN,
        programs=programs
    )
@socketio.on('createGroup')
def createGroup(group):
    # Send message to alls users
    print(group)

@socketio.on('createProgram')
def createProgram(group):
    # Send message to alls users
    print(group)


if __name__ == '__main__':
    socketio.run(app)
