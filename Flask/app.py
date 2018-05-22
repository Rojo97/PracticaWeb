import sys
import functools
from datetime import time, datetime
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
import functools
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
login_manager.login_message = u"Por favor logueate para acceder a esa pagina"
login_manager.login_message_category = "error"

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
    user = models.Usuario.query.filter_by(nickname=current_user.nickname).one()#filter_by(nickname=current_user.nickname).all()
    for n in user.grupos:
        groups.append({"id": n.grupoID, "name": n.nombre, "num": len(n.dispositivos), "class": n.clase, "desc": n.descripccion})

    return render_template(
        'index.html',
        domain=DOMAIN,
        groups=groups,
        current_user=current_user.nombre,
    )
@app.route('/newGroup')
@login_required
def new_groups_template():
    user = models.Usuario.query.filter_by(nickname=current_user.nickname).one()#filter_by(nickname=current_user.nickname).all()
    grupos = list(filter(lambda a: a.default == True,user.grupos))
    devices = grupos[0].dispositivos
    groups = models.Grupo.query.all()
    return render_template(
        'new-group.html',
        domain=DOMAIN,
        devices=devices,
        current_user=current_user.nombre,
        groups=groups,
        #TODO socketio+flask-login para no tener que mandar aqui el ID
        usuario=current_user.id

    )
@app.route('/group/<int:groupID>/update')
@login_required
def updateGroup(groupID):
    
    group = models.Grupo.query.filter_by(grupoID=groupID).one()
    devicesInGroup = group.dispositivos
    user = models.Usuario.query.filter_by(nickname=current_user.nickname).one()#filter_by(nickname=current_user.nickname).all()
    grupos = list(filter(lambda a: a.default == True,user.grupos))
    alldevices = grupos[0].dispositivos
    for i in devicesInGroup[:]:
        alldevices.remove(i)
    return render_template(
        'modificarDispGrupos.html',
        idgrupo = groupID,
        devicesInGroup = devicesInGroup,
        devicesNotInGroup = alldevices,
        domain=DOMAIN,        
        current_user=current_user.nombre,
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
def logout():
    logout_user()
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
@login_required
def new_sensor_template():
    group = request.args.get('group')
    if group == None:
        group = ''
    else:
        groupData = models.Grupo.query.filter_by(grupoID=group).one()
        group = groupData.nombre
    funciones = [
      {"name": "Luminosidad"},
      {"name": "Temperatura"},
      {"name": "Persianas"},
    ]
    tipos = [
      {"name": "Actuador"},
      {"name": "Sensor"},
    ]
    user = models.Usuario.query.filter_by(nickname=current_user.nickname).one()#filter_by(nickname=current_user.nickname).all()
    grupos = list(filter(lambda a: a.default == False,user.grupos))
    return render_template(
        'addSensor.html',
        domain=DOMAIN,
        current_user=current_user.nombre,
        funciones=funciones,
        tipos=tipos,
        grupos=grupos,
        default_group=group,
    )

@app.route('/addToGroup')
@login_required
def add_to_group_template():
    return render_template(
        'addToGroup.html',
        domain=DOMAIN,
        current_user=current_user.nombre,
    )

@app.route('/changePass')
@login_required
def change_pass_template():
    return render_template(
        'cambiarPassword.html',
        domain=DOMAIN,
        current_user=current_user.nombre,
    )

@app.route('/manageUserGroups')
@login_required
def manage_user_groups_template():
    usergroups = []
    usuarios = models.Usuario.query.all()
    groups = models.Grupo.query.all()
    user = models.Usuario.query.filter_by(nickname=current_user.nickname).one()
    for n in user.grupos:
        useraux = usuarios[:]
        group = list(filter(lambda a: a.grupoID==n.grupoID,groups))
        for s in group[0].usuarios:
            useraux.remove(s) 
        usergroups.append({"nousuarios":useraux,  "usuarios": group[0].usuarios, "id": n.grupoID, "name": n.nombre, "num": len(n.usuarios), "class": n.clase, "desc": n.descripccion})
            
    return render_template(

        'gestionarUsuariosGrupos.html',
        domain=DOMAIN,
        usergroups=usergroups,  
        users=usuarios,      
        current_user=current_user.nombre,
        current_nickname=current_user.nickname
    )

@app.route('/group/<int:groupID>')
@login_required
def group_template(groupID):
    group = models.Grupo.query.filter_by(grupoID=groupID).one()
    devices = group.dispositivos
    if group.default:
        default = 'true'
    else:
        default = 'false'
    return render_template(
        'grupos.html',
        idgrupo = groupID,
        groupName = group.nombre,
        default = default,
        devices = devices,
        domain=DOMAIN,
        current_user=current_user.nombre,
    )

@app.route('/newData')
@login_required
def new_data_template():
    sensores = models.Dispositivo.query.filter_by(tipo='Sensor').all()
    return render_template(
        'introducirDatos.html',
        domain=DOMAIN,
        sensores = sensores,
        current_user=current_user.nombre,
    )
@app.route('/newProgram')
@login_required
def new_program_template():
    actuadores = models.Dispositivo.query.filter_by(tipo='Actuador').all()
    return render_template(
        'newProgram.html',
        domain=DOMAIN,
        actuadores = actuadores,
        current_user=current_user.nombre,
    )
@app.route('/programs')
@login_required
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

#TODO integrar socketio con el login, para poder autentificar al usaurio dentro de esats funciones
#No es urgente, pero si queremos sacar esto a produccion es necesario (posible agujero de seguridad)

@socketio.on('createGroup')
def createGroup(group):
    
    newGroup = models.Grupo(
        nombre=group['name'],
        descripccion=group['desc'],
        default=False,
        clase='',
        
    )
    models.db.session.add(newGroup)
    print(current_user)
    try:
        models.db.session.flush()
        models.db.session.commit()
        newDetalle = models.DetalleMiembro(
            grupoID=newGroup.grupoID,
            nickname=group['user']
        )
        models.db.session.add(newDetalle)
        models.db.session.commit()
        for dispositivo in group['devices']:
            newDetalle = models.DetalleDispositivo(
                grupoID=newGroup.grupoID,
                disID=dispositivo
            )
            models.db.session.add(newDetalle)
            try:
                models.db.session.commit()
            except:
                models.db.session.rollback()
    except Exception as ex:
        print("Peligro: "+str(ex))
        models.db.session.rollback()    


@socketio.on('createProgram')
def createProgram(createProgram):
    print(createProgram)
    programaGrupo = models.ProgramaGrupo(
        nombre = createProgram['name'],
        descripccion = createProgram['desc']
    )
    models.db.session.add(programaGrupo)
    try:
        models.db.session.commit()
        for dispositivo in createProgram['devices']:
            newProgram = models.ProgramaIndividual(
                progGID=programaGrupo.progGID,
                disID=dispositivo['id'],
                valor=dispositivo['value'],
                fechaIni=time(hour=int(dispositivo['init'].split(':')[0]),minute=int(dispositivo['init'].split(':')[1]),second=0, microsecond=0),
                fechaFin=time(hour=int(dispositivo['end'].split(':')[0]),minute=int(dispositivo['end'].split(':')[1]), second=0, microsecond= 0)
            )
            models.db.session.add(newProgram)
            try:
                models.db.session.commit()
            except:
                models.db.session.rollback()
    except:
        models.db.session.rollback()
        return 0

@socketio.on('createMeasure')
def createMeasure(measure):
    print(measure)
    medida = models.Medicion(
        disID = measure['id'], 
        valor = measure['value'],
        fecha = datetime.strptime(measure['datetime'], '%d/%m/%Y-%H:%M').date()
    )
        # fecha = datetime(int(measure['datetime'].split('-')[0].split('/')[2]),
        #     int(measure['datetime'].split('-')[0].split('/')[1]),
        #     int(measure['datetime'].split('-')[0].split('/')[0]),
        #     int(measure['datetime'].split('-')[1].split(':')[0]),
        #     int(measure['datetime'].split('-')[1].split(':')[1])
        #     )
    models.db.session.add(medida)
    try:
        models.db.session.commit()
    except Exception as ex:
        print("Peligro: "+str(ex))
        models.db.session.rollback()

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
        newGroup = models.Grupo(
            nombre="Todos",
            descripccion="Todos mis dispositivos",
            default=True,
            clase='',
        )
        models.db.session.add(newGroup)
        models.db.session.flush()
        print("Id del nuevo grupo:"+str(newGroup.grupoID))
        models.db.session.commit()
        print("Id del nuevo grupo:"+str(newGroup.grupoID))

        newDetalle = models.DetalleMiembro(
            grupoID=newGroup.grupoID,
            nickname=newUser.nickname
            
        )
        models.db.session.add(newDetalle)
        models.db.session.commit()   
    except Exception as ex:
        print(ex)
        models.db.session.rollback()
        emit('userNotCreated')

    # try:
        # models.db.session.commit()
    # except:
    #     models.db.session.rollback()
@socketio.on('createSensor')
def createSensor(sensor):
    print(sensor)
    newSensor = models.Dispositivo(
        nombre=sensor['name'],
        tipo=sensor['tipo'],
        estado=0,
        clase='',
        funcion = sensor['funcion']
    )
    models.db.session.add(newSensor)
    models.db.session.flush()
    try:
        models.db.session.commit()
        if sensor['grupo'] != -1:
            newDetalle = models.DetalleDispositivo(
                grupoID=sensor['grupo'],
                disID=newSensor.disID
            )
            models.db.session.add(newDetalle)
            models.db.session.commit()
        user = models.Usuario.query.filter_by(nickname=current_user.nickname).one()#filter_by(nickname=current_user.nickname).all()
        grupos = list(filter(lambda a: a.default == True,user.grupos))
    
        newDetalle = models.DetalleDispositivo(
            grupoID=grupos[0].grupoID,
            disID=newSensor.disID
        )
        models.db.session.add(newDetalle)
        models.db.session.commit()
    except:
        models.db.session.rollback()

    # try:
        # models.db.session.commit()
    # except:
    #     models.db.session.rollback()

@socketio.on('addGroupUser')
def addGroupUser(data):
    group_id = data['groupId']
    user_nickname = data['userNickname']

    with app.app_context():
        try:
            newDetalle = models.DetalleMiembro(
                grupoID = group_id,
                nickname = user_nickname
            )
            models.db.session.add(newDetalle)
            models.db.session.commit()
            emit('addedGroupUser', data)
        except Exception as ex:
            print("Error:", ex)
            models.db.session.rollback()
            emit('notAddedGroupUser')

@socketio.on('removeGroupUser')
def removeGroupUser(data):
    group_id = data['groupId']
    user_nickname = data['userNickname']

    with app.app_context():
        try:
            models.DetalleMiembro.query.filter_by(
                grupoID = group_id,
                nickname = user_nickname
            ).delete()
            models.db.session.commit()
            emit('removedGroupUser', data)
        except Exception as ex:
            print("Error:", ex)
            models.db.session.rollback()
            emit('notRemovedGroupUser')


@socketio.on('addDeviceToGroup')
def addDeviceToGroup(devices):
    try:
        for i in devices['added'][:]:
            newDetalle = models.DetalleDispositivo(
                grupoID=devices['grupo'],
                disID=i
            )
            models.db.session.add(newDetalle)
            models.db.session.commit()
        emit('reload')
    except:
        models.db.session.rollback()

@socketio.on('removeDeviceFromGroup')
def removeDeviceFromGroup(devices):
    try:
        for i in devices['removed'][:]:
            detalle = models.DetalleDispositivo.query.filter_by(grupoID=devices['grupo'],disID=i).one()
            models.db.session.delete(detalle)
            models.db.session.commit()
        emit('reload')
    except Exception as ex:
        print(ex)
        models.db.session.rollback()
    
@socketio.on('cambiarEstadoLuz')
def cambiarEstadoLuz(device):
    print("Hola")
    disp = models.Dispositivo.query.filter_by(disID=device['id']).one()
    print(">>>", disp.estado)

    if disp.estado==0.0:
        with app.app_context():
            disp.estado = 1.0
            models.db.session.commit()
            emit('reload',models.model_to_dict(disp, models.Dispositivo))
    else:
        with app.app_context():
            disp.estado = 0.0
            models.db.session.commit()
            emit('reload',models.model_to_dict(disp, models.Dispositivo))
@socketio.on('cambiarEstado')
def cambiarEstado(device):
    print("Hola")
    disp = models.Dispositivo.query.filter_by(disID=device['id']).one()
    print(">>>", disp.estado)
    try:
        valor=float(device['newValue'])
        pass
    except:
        return
    if disp.funcion == 'Persianas':
        if valor > 100.0:
            valor=100.0
        if valor < 0.0:
            valor=0.0
        else:
            valor=round(valor,0)
    else:
        if valor > 30.0:
            valor=30.0
        if valor < 10.0:
            valor=10.0
        else:
            valor=round(valor,1)
    with app.app_context():
        disp.estado = valor
        models.db.session.commit()
        emit('reload',models.model_to_dict(disp, models.Dispositivo))


    
if __name__ == '__main__':
    socketio.run(app)
