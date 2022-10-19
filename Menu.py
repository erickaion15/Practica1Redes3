
import os
from time import sleep
import time
from Agente import *
from consulta import *
from Monitor import *
import threading
from Reporte import *
import shutil


#OIDS
NUMERO_DE_INTERFACES = '1.3.6.1.2.1.2.1.0'
INFORMACION_INTERFAZ = '1.3.6.1.2.1.2.2.1.2.'
ESTADO_INTERFAZ = '1.3.6.1.2.1.2.2.1.7.'

class Menu:

    def Accion(opcion,hosts):
        if(opcion == 1):
            os.system ("clear")
            print('AGREGAR AGENTE'.center(40,'*'))
            hostname = input('Introduce el Hostname: ')
            version = int(input('Introduce la version: '))
            comunidad = input('Introduce la comunidad: ')
            puerto = int(input('Introduce el puerto: '))
            a = Agente(hostname,version,comunidad,puerto)
            a.addAgente()
            Menu()


        elif(opcion==2):
            os.system ("clear")
            print('ELIMINAR AGENTE'.center(40,'*'))
            hostname = input('Introduce el Hostname: ')
            Agente.deleteAgente(hostname)
            try:
                shutil.rmtree(hostname)
            except Exception as e:
                print(str(e))
            sleep(3)
            Menu()
        elif(opcion==3):
            print('Crear Reporte')
            print('Hostnames disponibles para crear un reporte')
            for i in hosts:
                print('*',i[0])
            hostname = input('Introduce el nombre del hostname:')
            hostname = Agente.getAgente(hostname)
            
            r = Reporte(hostname)
            r.CrearReporte()
            print("Se ha creado exitosamente el Reporte del hostname:",hostname[0])
            sleep(3)
            Menu()

        elif(opcion==4):
            os.system ("clear")
            quit()
        else:
            os.system ("clear")
            print('Teclea una opcion correcta'.center(40,'*'))
            Menu()


    def Opciones(hosts):
        print('Que opcion deseas realizar?')
        print('1-Agregar Agente')
        print('2-Eliminar Agente')
        print('3-Realizar un reporte')
        print('4-Salir')
        opcion = int(input("Digite un numero: "))
        Menu.Accion(opcion,hosts)

    def __init__(self):
        self.host_disponibles = []
        os.system ("clear")
        agentes = Agente.getAgentes()
        print('RESUMEN'.center(20,'-'))
        print('Host en monitoreo:',len(agentes))
        if(len(agentes)!=0):
            for i in agentes:
                numero_interfaces = consulta(i[0],i[1],i[2],i[3],NUMERO_DE_INTERFACES)
                estado = 'UP' if numero_interfaces != False else 'DOWN'
                print('*Hostname:',i[0])
                if(numero_interfaces == False):
                    numero_interfaces = 'DOWN'
                    print('Numero de Interfaces:',numero_interfaces)
                    print('Estado del Agente:',estado)
                else:
                    print('Numero de Interfaces:',numero_interfaces)
                    print('Estado del Agente:',estado)
                    self.host_disponibles.append(i)
                    print('**Lista de Interfaces**')
                    for interfaz in range(1,int(numero_interfaces)<5):

                        descripcion = str(consulta(i[0],i[1],i[2],i[3],INFORMACION_INTERFAZ+str(interfaz)))
                        interfaz_estado = int(consulta(i[0],i[1],i[2],i[3],ESTADO_INTERFAZ+str(interfaz)))
                        descripcion = getDescription(descripcion)
                        interfaz_estado = 'UP' if interfaz_estado == 1 else 'DOWN'
                        print('No:',interfaz,descripcion,'-Estado:',interfaz_estado)
        else:
            print('No hay ningun Host dado de alta')
        #print(self.host_disponibles)
        m = Monitor(self.host_disponibles)
        m.CrearCarpetas()
        m.CrearRRD()
        hilo = threading.Thread(target=m.Update,)
        hilo2 = threading.Thread(target=Menu.Opciones,args=(self.host_disponibles,),)
        #Menu.Opciones(self.host_disponibles)
        hilo.start()
        hilo2.start()
        
        

if(__name__ == '__main__'):

    Menu()
