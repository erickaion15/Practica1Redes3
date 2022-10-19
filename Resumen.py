import os
from time import sleep
from Agente import *
from consulta import *


#OIDS
NUMERO_DE_INTERFACES = '1.3.6.1.2.1.2.1.0'
INFORMACION_INTERFAZ = '1.3.6.1.2.1.2.2.1.2.'
ESTADO_INTERFAZ = '1.3.6.1.2.1.2.2.1.7.'

i = ['192.168.1.74',1,'comunidadASR',161]
numero_interfaces = consulta(i[0],i[1],i[2],i[3],NUMERO_DE_INTERFACES)
estado = 'UP' if numero_interfaces != False else 'DOWN'
print('*Hostname:',i[0])
print('Numero de Interfaces:',numero_interfaces)
print('Estado del Agente:',estado)
print('**Lista de Interfaces**')
for interfaz in range(1,int(numero_interfaces)+1):

    descripcion = (consulta(i[0],i[1],i[2],i[3],INFORMACION_INTERFAZ+str(interfaz)))
    interfaz_estado = int(consulta(i[0],i[1],i[2],i[3],ESTADO_INTERFAZ+str(interfaz)))
    #descripcion = bytes.fromhex(descripcion).decode('utf-8')
    interfaz_estado = 'UP' if interfaz_estado == 1 else 'DOWN'
    print('No:',interfaz,descripcion,'-Estado:',interfaz_estado)
    print('*****',(consulta(i[0],i[1],i[2],i[3],INFORMACION_INTERFAZ+str(interfaz))))

