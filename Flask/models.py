# -*- coding: utf-8 -*-
# Librarys
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from os import environ
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import Column, Date, Float, ForeignKey, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(find_dotenv())
app = Flask(__name__)

# Settings
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Variables
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

Base = declarative_base()
metadata = Base.metadata
'''
t_DetalleDispositivo = Table(
    'DetalleDispositivo', metadata,
    Column('grupoID',String(10), ForeignKey('grupo.grupoID')),
    Column('disID',String(10), ForeignKey('dispositivo.disID'))
)

t_DetalleMiembro = Table(
    'DetalleMiembro', metadata,
    Column('nickname',String(10), ForeignKey('usuario.nickname')),
    Column('grupoID',String(10), ForeignKey('grupo.grupoID'))
)
'''

class DetalleDispositivo(db.Model):
    __tablename__ = 'detalleDispositivo'

    grupoID = Column(ForeignKey('grupo.grupoID'), primary_key=True, index=True)
    disID = Column(ForeignKey('dispositivo.disID'), primary_key=True, index=True)

class DetalleMiembro(db.Model):
    __tablename__ = 'detalleMiembro'

    grupoID = Column(ForeignKey('grupo.grupoID'), primary_key=True, index=True)
    nickname = Column(ForeignKey('usuario.nickname'), primary_key=True, index=True)

class Usuario(db.Model):
    __tablename__ = 'usuario'

    nickname = Column(String(10), primary_key=True)
    nombre = Column(String(20), nullable=False)
    contraseña = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)


class Grupo(db.Model):
    __tablename__ = 'grupo'

    grupoID = Column(String(10), primary_key=True)
    nombre = Column(String(20), nullable=False)
    descripccion = Column(String(200), nullable=False)
    clase = Column(String(40), nullable=False)

    usuarios = relationship('Usuario', secondary='detalleMiembro',
        backref=backref('grupos', lazy=True))



class Dispositivo(db.Model):
    __tablename__ = 'dispositivo'

    disID = Column(String(10), primary_key=True)
    tipo = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)

    grupos = relationship('Grupo', secondary='detalleDispositivo',
        backref=backref('dispositivos', lazy=True))



class Medicion(db.Model):
    __tablename__ = 'medicion'

    medID = Column(String(10), primary_key=True)
    disID = Column(ForeignKey('dispositivo.disID'), index=True)
    valor = Column(Float(asdecimal=True), nullable=False)
    fecha = Column(Date, nullable=False)

    Dispositivo = relationship('Dispositivo')


class ProgramaGrupo(db.Model):
    __tablename__ = 'programaGrupo'

    progGID = Column(String(10), primary_key=True)
    grupoID = Column(ForeignKey('grupo.grupoID'), index=True)
    nombre = Column(String(20), nullable=False)
    descripccion = Column(String(200), nullable=True)

    Grupo = relationship('Grupo')


class ProgramaIndividual(db.Model):
    __tablename__ = 'programaIndividual'

    progIID = Column(String(10), primary_key=True)
    progGID = Column(ForeignKey('programaGrupo.progGID'), index=True)
    disID = Column(ForeignKey('dispositivo.disID'), index=True)
    valor = Column(Float(asdecimal=True), nullable=False)
    fechaIni = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=False)

    Dispositivo = relationship('Dispositivo')
    ProgramaGrupo = relationship('ProgramaGrupo')


if __name__ == "__main__":
    manager.run()