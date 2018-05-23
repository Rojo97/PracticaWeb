#!/bin/bash

rm -rf __pycache__/

rm -rf migrations/

rm database.sqlite

python3 models.py db init

python3 models.py db migrate

python3 models.py db upgrade

sqlite3 database.sqlite -batch $1 <<"EOF"

INSERT INTO USUARIO (nickname,nombre,active,contraseña,email) VALUES ('isma', 'ismael', TRUE, 'pbkdf2:sha256:50000$1bsB5ZXW$6cbd8619e0349a499b092ec5835c747050327d3b584b3c217e437e82be961b26', 'ismi_loco@hotmail.com');

INSERT INTO GRUPO (grupoID,nombre,descripccion,clase) VALUES (1, 'todos', 'aaaaaa', '1');

INSERT INTO DETALLEMIEMBRO (grupoID,nickname) VALUES (1, 'isma');

INSERT INTO DISPOSITIVO (disID,nombre,tipo,estado,funcion,clase) VALUES (1,'luz1','Actuador',0.0,'Luminosidad','a');

INSERT INTO DETALLEDISPOSITIVO (grupoID,disID) VALUES (1,1);

INSERT INTO PROGRAMAGRUPO (progGID, grupoID, nombre, descripccion) VALUES (1,1,'prueba1','descrip');

INSERT INTO PROGRAMAGRUPO (progGID, grupoID, nombre, descripccion) VALUES (2,1,'prueba2','descrip2'); 

.exit

EOF

python3 app.py
