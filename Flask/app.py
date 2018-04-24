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
models.db.init_app(app)

@app.route('/groups')
def groups_template():
    groups = []
    '''
    allgroups = models.Grupo.query(all)
    for n in allgroups:
        groups.append({"id": n.grupoID, "name": n.nombre, "num": len(n.sensores), "class": n.clase})

    '''
    return render_template(
        'index.html',
        domain=DOMAIN,
        groups=groups
    )
@app.route('/newGroup')
def new_groups_template():
    devices = models.Dispositivo.query.all()
    groups = models.Grupo.query.all()
    '''
    devices = [
      { "id": 1, "name": "Luces de la cochera", "type": "light"},
      { "id": 2, "name": "Luces del salon", "type": "light"},
      { "id": 3, "name": "Temperatura del salon", "type": "thermostat"},
      { "id": 4, "name": "Luces de la cocina", "type": "light"},
      { "id": 5, "name": "Temperatura de la cocina", "type": "thermostat"},
    ]
    groups = [
      { "id": 1, "name": "Todos", "class": "fa-calendar-minus-o"},
      { "id": 2, "name": "Salón", "class": "fa-home"},
      { "id": 3, "name": "Cocina", "class": "fa-home"},
      { "id": 4, "name": "Pasillo", "class": "fa-home"},
      { "id": 5, "name": "Luces", "class": "fa-lightbulb-o"}
    ]
    '''
    return render_template(
        'new-group.html',
        domain=DOMAIN,
        devices=devices,
        groups=groups
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
    funciones = [
      { "id": 1, "funcion": "Cochera", "name": "Luminosidad", "type": "light"},
      { "id": 2, "funcion": "Salón", "name": "Temperatura", "type": "light"},
      { "id": 3, "funcion": "Salón", "name": "Persianas", "type": "thermostat"},
    ]
    tipos = [
      {"name": "Actuador"},
      {"name": "Sensor"},
    ]
    grupos = [
      { "id": 1, "funcion": "Cochera", "name": "Grupo 1", "type": "light"},
      { "id": 2, "funcion": "Salón", "name": "Grupo 2", "type": "light"},
      { "id": 3, "funcion": "Salón", "name": "Grupo 3", "type": "thermostat"},
      { "id": 4, "funcion": "Cocina", "name": "Grupo 4", "type": "light"},
      { "id": 5, "funcion": "Cocina", "name": "Grupo 5", "type": "thermostat"},
    ]
    return render_template(
        'addSensor.html',
        domain=DOMAIN,
        funciones=funciones,
        tipos=tipos,
        grupos=grupos
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
    devices = [
        { "disID": 1, "nombre": "Luces de la cochera", "funcion": "Luminosidad", "estado": "1"},
        { "disID": 2, "nombre": "Luces de la cochera", "funcion": "Luminosidad", "estado": "1"},
        { "disID": 3, "nombre": "Temperatura del salon", "funcion": "Luminosidad", "estado": "1"},
        { "disID": 4, "nombre": "Luces de la cocina", "funcion": "Luminosidad", "estado": "1"},
        { "disID": 5, "nombre": "Temperatura de la cocina", "funcion": "Luminosidad", "estado": "1"}
    ]
    return render_template(
        'grupos.html',
        devices = devices,
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
