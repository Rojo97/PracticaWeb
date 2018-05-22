# -*- coding: utf-8 -*-
# Librarys
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from os import environ
from dotenv import load_dotenv, find_dotenv
# from flask_security import Security, SQLAlchemyUserDatastore, \
from flask_login import UserMixin

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Table, Integer, Boolean, Time
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

class DetalleDispositivo(db.Model):
    __tablename__ = 'detalleDispositivo'

    grupoID = Column(ForeignKey('grupo.grupoID'), primary_key=True, index=True)
    disID = Column(ForeignKey('dispositivo.disID'), primary_key=True, index=True)

class DetalleMiembro(db.Model):
    __tablename__ = 'detalleMiembro'

    grupoID = Column(ForeignKey('grupo.grupoID'), primary_key=True, index=True)
    nickname = Column(ForeignKey('usuario.nickname'), primary_key=True, index=True)

class Usuario(db.Model,UserMixin):
    __tablename__ = 'usuario'

    nickname = Column(String(20), primary_key=True)
    nombre = Column(String(255), nullable=False)
    active = Column(Boolean())
    contraseña = Column(String(400), nullable=False)
    email = Column(String(50), nullable=False, unique=True)

    @property
    def id(self):
        return self.nickname




class Grupo(db.Model):
    __tablename__ = 'grupo'

    grupoID = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(40), nullable=False)
    descripccion = Column(String(200), nullable=True)
    clase = Column(String(40), nullable=False)
    default = Column(Boolean())

    usuarios = relationship('Usuario', secondary='detalleMiembro',
        backref=backref('grupos', lazy=True))

    programas = relationship('ProgramaGrupo',
        backref=backref('grupo', lazy=True))

    #programa = relationship('ProgramaGrupo', back_populates='gruporef')
    #progs = relationship("ProgramaGrupo", back_populates="grup")



class Dispositivo(db.Model):
    __tablename__ = 'dispositivo'

    disID = db.Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(40), nullable=False)
    tipo = Column(String(20), nullable=False)
    estado = Column(Float, nullable=False)
    clase = Column(String(40), nullable=False)
    funcion = Column(String(20), nullable=False)

    grupos = relationship('Grupo', secondary='detalleDispositivo',
        backref=backref('dispositivos', lazy=True))



class Medicion(db.Model):
    __tablename__ = 'medicion'

    medID = Column(Integer, primary_key=True,autoincrement=True)
    disID = Column(ForeignKey('dispositivo.disID'), index=True)
    valor = Column(Float(asdecimal=True), nullable=False)
    fecha = Column(DateTime, nullable=False)

    Dispositivo = relationship('Dispositivo')


class ProgramaGrupo(db.Model):
    __tablename__ = 'programaGrupo'

    progGID = Column(Integer, primary_key=True,autoincrement=True)
    grupoID = Column(ForeignKey('grupo.grupoID'), index=True)
    nombre = Column(String(20), nullable=False)
    descripccion = Column(String(200), nullable=True)

    group = relationship("Grupo")

    subprogramas = relationship('ProgramaIndividual',
        backref=backref('prog', lazy=True))

    #grupo = relationship('Grupo')


class ProgramaIndividual(db.Model):
    __tablename__ = 'programaIndividual'

    progIID = Column(Integer, primary_key=True,autoincrement=True)
    progGID = Column(ForeignKey('programaGrupo.progGID'), index=True)
    disID = Column(ForeignKey('dispositivo.disID'), index=True)
    valor = Column(Float(asdecimal=True), nullable=False)
    fechaIni = Column(Time, nullable=False)
    fechaFin = Column(Time, nullable=False)

    Dispositivo = relationship('Dispositivo')
    ProgramaGrupo = relationship('ProgramaGrupo')

def model_to_dict(inst, cls):
  """
  Jsonify the sql alchemy query result. Skips attr starting with "_"
  """
  convert = {}
  d = dict()
  for c in cls.__table__.columns:
    if c.name.startswith("_"):
      continue
    v = getattr(inst, c.name)
    current_type = str(c.type)
    if current_type in convert.keys() and v is not None:
      try:
        d[c.name] = convert[current_type](v)
      except:
        d[c.name] = "Error:  Failed to covert using ", unicode(convert[c.type])
    elif v is None:
      d[c.name] = unicode()
    else:
      d[c.name] = v
  return d

if __name__ == "__main__":
    manager.run()
