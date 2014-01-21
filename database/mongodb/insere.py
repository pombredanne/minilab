# -*- coding: utf-8 -*-
from database.mongodb import conexion

conexion.conecta()

assert conexion.cnx is not None

cliente = conexion.base.cliente

while True:
    nombre = raw_input('Nombre:')
    email = raw_input('Correo electrónico:')
    pais = raw_input('País:')
    ciudad = raw_input('Ciudad:')
    telefono = raw_input('Teléfono:')
    interes = raw_input('Interés:')

    cliente.insert({'nombre': nombre,
                    'email': email,
                    'pais': pais,
                    'ciudad': ciudad,
                    'telefono': telefono,
                    'interes': interes})
    print 'Dados registrados.'

    if raw_input('Deseja catastrar un nuevo registro (s/n)') == 'n': break
