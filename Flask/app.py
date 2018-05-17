import sys
from os import environ
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect,url_for, abort, request, flash
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import models
from flask import request
# from flask_security import Security, SQLAlchemyUserDatastore, \
from flask_login import login_required, login_user, logout_user,\
    current_user
from flask_login import LoginManager
from wtforms import Form, TextField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash

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

# Setup Flask-Security
# user_datastore = SQLAlchemyUserDatastore(models.db, models.User)
# security = Security(app, user_datastore)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_template"

@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.Usuario.query.filter_by(nickname=user_id).one()
    except:
        user = None
    return user

@app.route('/groups')
@login_required
def groups_template():
    groups = []
    devices = models.Dispositivo.query.all()
    allgroups = models.Grupo.query.all()
    for n in allgroups:
        groups.append({"id": n.grupoID, "name": n.nombre, "num": len(n.dispositivos), "class": n.clase, "desc": n.descripccion})
    
    return render_template(
        'index.html',
        domain=DOMAIN,
        groups=groups,
        current_user=current_user.nombre,
        dispositivostotal=len(devices)
    )
@app.route('/newGroup')
@login_required
def new_groups_template():
    
    devices = models.Dispositivo.query.all()
    groups = models.Grupo.query.all()
    '''
    devices = [
      { "disID": 1, "nombre": "Luces de la cochera", "funcion": "Luminosidad"},
      { "disID": 2, "nombre": "Luces de la cochera", "funcion": "Luminosidad"},
      { "disID": 3, "nombre": "Temperatura del salon", "funcion": "Luminosidad"},
      { "disID": 4, "nombre": "Luces de la cocina", "funcion": "Luminosidad"},
      { "disID": 5, "nombre": "Temperatura de la cocina", "funcion": "Luminosidad"},
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
        current_user=current_user.nombre,
        groups=groups
    )

class LoginForm(Form):
    email = TextField('email', [validators.Required()])
    password = PasswordField('password', [validators.Required()])

@app.route('/', methods=['GET', 'POST'])
def login_template():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = models.Usuario.query.filter_by(email=form.email.data.lower()).first()
        if user:
            if check_password_hash(user.contraseña, form.password.data):
                if login_user(user):
                    print('Logged in user %s', user.nickname)
                    

                    next = request.args.get('next')
                    # is_safe_url should check if the url is safe for redirects.
                    # See http://flask.pocoo.org/snippets/62/ for an example.
                    # TODO: error `pip install urlparse`
                    # if not is_safe_url(next):
                    #     return abort(400)

                    return redirect(next or url_for('groups_template'))
            else:
                flash('Contraseña incorrecta.','error')

        else:
            flash('El usuario no existe.','error')

    return render_template(
        'login2.html',
        domain=DOMAIN
    )

@app.route('/logout')
@login_required
def logout_pixas():
    print('logout', current_user, end='')
    logout_user()
    print(current_user)
    return redirect(url_for('login_template'))


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
    group = request.args.get('group')
    if group == None or group == 0:
        group = ''
    else:
        groupData = models.Grupo.query.filter_by(grupoID=group).all()
        group = group+'- '+groupData[0].nombre
    funciones = [
      {"name": "Luminosidad"},
      {"name": "Temperatura"},
      {"name": "Persianas"},
    ]
    tipos = [
      {"name": "Actuador"},
      {"name": "Sensor"},
    ]
    groups = models.Grupo.query.all()
    return render_template(
        'addSensor.html',
        domain=DOMAIN,        
        current_user=current_user.nombre,
        funciones=funciones,
        tipos=tipos,
        grupos=groups,
        default_group=group
    )

@app.route('/addToGroup')
def add_to_group_template():
    return render_template(
        'addToGroup.html',
        domain=DOMAIN,        
        current_user=current_user.nombre,
    )

@app.route('/changePass')
def change_pass_template():
    return render_template(
        'cambiarPassword.html',
        domain=DOMAIN,        
        current_user=current_user.nombre,
    )

@app.route('/manageUserGroups')
def manage_user_groups_template():
    return render_template(
        'gestionarUsuariosGrupos.html',
        domain=DOMAIN,        
        current_user=current_user.nombre,
    )

@app.route('/group/<int:groupID>')
def group_template(groupID):
    if groupID!=0:
        group = models.Grupo.query.filter_by(grupoID=groupID).all()
        devices = group[0].dispositivos
    else:
        devices = models.Dispositivo.query.all()

    return render_template(
        'grupos.html',
        idgrupo = groupID,
        devices = devices,
        domain=DOMAIN,        
        current_user=current_user.nombre,
    )

@app.route('/newData')
def new_data_template():
    return render_template(
        'introducirDatos.html',
        domain=DOMAIN,        
        current_user=current_user.nombre,
    )
@app.route('/newProgram')
def new_program_template():
    actuadores = models.Dispositivo.query.filter_by(tipo='Actuador').all()

    # actuadores = [
    #   { "id": 1, "name": "Todos", "num": 26, "class": "fa-calendar-minus-o"},
    #   { "id": 2, "name": "Salón", "num": 5, "class": "fa-home"},
    #   { "id": 3, "name": "Cocina", "num": 3, "class": "fa-home"},
    #   { "id": 4, "name": "Pasillo", "num": 2, "class": "fa-home"},
    #   { "id": 5, "name": "Luces", "num": 14, "class": "fa-lightbulb-o"}
    # ]
    return render_template(
        'newProgram.html',
        domain=DOMAIN,
        actuadores = actuadores,        
        current_user=current_user.nombre,
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
        programs=programs,        
        current_user=current_user.nombre,
    )
@socketio.on('createGroup')
def createGroup(group):
    # Send message to alls users
    
    newGroup = models.Grupo(
        nombre=group['name'],
        descripccion=group['desc'],
        clase='',
    )
    models.db.session.add(newGroup)
    try:
        models.db.session.commit()
        grupoGenerado= models.Grupo.query.all()[-1].grupoID
        for dispositivo in group['devices']:
            newDetalle = models.DetalleDispositivo(
                grupoID=grupoGenerado,
                disID=dispositivo.split('-')[0]
            )
            models.db.session.add(newDetalle)
            try:
                models.db.session.commit()
            except:
                models.db.session.rollback()
    except:
        models.db.session.rollback()    


@socketio.on('createProgram')
def createProgram(createProgram):
    # newProgram = mocreateProgramdels.ProgramaGrupo(
    #     grupoID=0
    #     nombre=createProgram['name'],
    #     descripccion=createProgram['desc']
    # )
    # models.db.session.add(newGroup)
    # try:
    #     models.db.session.commit()
    # except:
    #     models.db.session.rollback()
    #     return 1
    print()

@socketio.on('createUser')
def createUser(user):
    print(user)
    '''
    TODO
    if usuario existe
        emit('userUsed')
        emit('userNotCreated')
    if email existe
        emit('emailUsed')
        emit('userNotCreated')
    '''
    newUser = models.Usuario(
        nickname = user['username'],
        nombre = user['name'],
        contraseña = generate_password_hash(user['password']),
        active=True,
        email = user['email']
    )
    models.db.session.add(newUser)
    try:
        models.db.session.commit()
        emit('userCreated')

    except Exception as ex:
        print(ex)
        models.db.session.rollback()
        emit('userNotCreated')
    
    # try:
        # models.db.session.commit()
    # except:
    #     models.db.session.rollback()
@socketio.on('loginUser')
def loginUser(user):
    print(user)
    try:
        user = models.Usuario.query.filter_by(email=user['email']).one()
        #TODO que sea un login de verdad
        print(user)
        with app.app_context():
            login_user(user, remember=True)
        print(current_user)
        emit('loggedIn')
    except Exception as ex:
        print("Esto falla puto:")
        print(ex)
        #TODO mensaje de error

@socketio.on('logoutUser')
def logoutUser():
    print()
    try:
        
        logout_user()
        emit('loggedOut')
    except Exception as ex:
        print("Esto falla puto:")
        print(ex)
        #TODO mensaje de error


@socketio.on('createSensor')
def createSensor(sensor):
    # Send message to alls users
    print(sensor)
    newSensor = models.Dispositivo(
        nombre=sensor['name'],
        tipo=sensor['tipo'],
        estado=0,
        clase='',
        funcion = sensor['funcion']
    )
    models.db.session.add(newSensor)
    try:
        models.db.session.commit()
        disGenerado= models.Dispositivo.query.all()[-1].disID
        newDetalle = models.DetalleDispositivo(
            grupoID=sensor['grupo'].split('-')[0],
            disID=disGenerado
        )
        models.db.session.add(newDetalle)
        try:
            models.db.session.commit()
        except:
            models.db.session.rollback()
    except:
        models.db.session.rollback()
    
    # try:
        # models.db.session.commit()
    # except:
    #     models.db.session.rollback()
if __name__ == '__main__':
    socketio.run(app)
