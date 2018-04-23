#-*- coding: utf-8 -*-
# Librarys
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from os import environ
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import Column, Date, Float, ForeignKey, String, Table
from sqlalchemy.orm import relationship
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

'''
class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    text = db.Column(db.Text)
    channel = db.Column(db.Integer)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Chat {0}>'.format(self.username)

'''

Base = declarative_base()
metadata = Base.metadata


t_DetalleDispositivo = Table(
    'DetalleDispositivo', metadata,
    Column('grupoID', ForeignKey('Grupo.grupoID'), primary_key=True, nullable=False),
    Column('disID', ForeignKey('Dispositivo.disID'), primary_key=True, nullable=False, index=True)
)


t_DetalleMiembro = Table(
    'DetalleMiembro', metadata,
    Column('nickname', ForeignKey('Usuario.nickname'), primary_key=True, nullable=False),
    Column('grupoID', ForeignKey('Grupo.grupoID'), primary_key=True, nullable=False, index=True)
)


class Dispositivo(db.Model):
    __tablename__ = 'Dispositivo'

    disID = Column(String(10), primary_key=True)
    tipo = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)

    Grupo = relationship('Grupo', secondary='DetalleDispositivo')


class Grupo(db.Model):
    __tablename__ = 'Grupo'

    grupoID = Column(String(10), primary_key=True)
    nombre = Column(String(20), nullable=False)
    descripccion = Column(String(200), nullable=False)

    Usuario = relationship('Usuario', secondary='DetalleMiembro')


class Medicion(db.Model):
    __tablename__ = 'Medicion'

    medID = Column(String(10), primary_key=True)
    disID = Column(ForeignKey('Dispositivo.disID'), index=True)
    valor = Column(Float(asdecimal=True), nullable=False)
    fecha = Column(Date, nullable=False)

    Dispositivo = relationship('Dispositivo')


class ProgramaGrupo(db.Model):
    __tablename__ = 'ProgramaGrupo'

    progGID = Column(String(10), primary_key=True)
    grupoID = Column(ForeignKey('Grupo.grupoID'), index=True)
    nombre = Column(String(20), nullable=False)
    descripccion = Column(String(200), nullable=True)

    Grupo = relationship('Grupo')


class ProgramaIndividual(db.Model):
    __tablename__ = 'ProgramaIndividual'

    progIID = Column(String(10), primary_key=True)
    progGID = Column(ForeignKey('ProgramaGrupo.progGID'), index=True)
    disID = Column(ForeignKey('Dispositivo.disID'), index=True)
    valor = Column(Float(asdecimal=True), nullable=False)
    fechaIni = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=False)

    Dispositivo = relationship('Dispositivo')
    ProgramaGrupo = relationship('ProgramaGrupo')


class Usuario(db.Model):
    __tablename__ = 'Usuario'

    nickname = Column(String(10), primary_key=True)
    nombre = Column(String(20), nullable=False)
    contraseña = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)


if __name__ == "__main__":
    manager.run()
