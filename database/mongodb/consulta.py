# -*- coding: utf-8 -*-
from database.mongodb import conexion

conexion.conecta()

assert conexion.cnx is not None

cliente = conexion.base.cliente

print 'Lista de Clientes'
for item in cliente.find():
    print u'Nombre: %(nombre)s; Teléfono: %(telefono)s; E-mail: %(email)s; Interés: %(interes)s' % item
