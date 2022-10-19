import sqlite3


class Agente:

    def __init__(self,hostname,version,comunidad,puerto):
        self.hostname = hostname
        self.version = version
        self.comunidad = comunidad
        self.puerto = puerto
    
    def __str__(self):
        return f'{self.hostname}-{self.comunidad}'

    def addAgente(self):
        conexion=sqlite3.connect("Agentes.db")
        try:
            conexion.execute(f'''
            CREATE TABLE IF NOT EXISTS agente
            (
                hostname varchar(25) PRIMARY KEY NOT NULL,
                version int NOT NULL,
                comunidad varchar(25) NOT NULL,
                puerto  int NOT NULL
                );''')
            
            conexion.execute(f'''
                INSERT INTO `agente` (`hostname`, `version`, `comunidad`, `puerto`) 
                VALUES ('{self.hostname}', '{self.version}', '{self.comunidad}', '{self.puerto}');
            ''')
            print('Se ha creado el siguiente hostname',self.hostname)
            conexion.commit()
        except Exception as e:
            print(str(e))
        conexion.close()
    

    def deleteAgente(hostname):
        conexion=sqlite3.connect("Agentes.db",timeout=10)
        
        try:
            conexion.execute(f'''
            DELETE FROM `agente` WHERE `agente`.`hostname` = '{hostname}';
            ''')
            conexion.commit()
            print("Se ha eliminado con exito el hostname:",hostname)
        except Exception as e:
            print(str(e))
        conexion.close()

    def getAgentes():
        conexion=sqlite3.connect("Agentes.db",timeout=10)
        agentes = []
        try:
            cursor=conexion.execute("SELECT * FROM agente;")
            for fila in cursor:
                agentes.append(list(fila))
        except Exception as e:
            print(str(e))
        conexion.close()
        return agentes

    def getAgente(hostname):
        conexion=sqlite3.connect("Agentes.db",timeout=10)
        agente = []
        try:
            cursor=conexion.execute(f"SELECT * FROM agente where hostname = '{hostname}';")
            for fila in cursor:
                agente.append(list(fila))
        except Exception as e:
            print(str(e))
        conexion.close()
        return agente[0]

if(__name__ == '__main__'):
    print(Agente.getAgente('localhost'))
    #Agente.deleteAgente('192.168.1.0')
    