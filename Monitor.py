from os import *
import sys
import rrdtool
import time
from ConsultaExterna import *
from consulta import*


PACKET_MULTICAST_INT = '1.3.6.1.2.1.2.2.1.12.'
NUMERO_DE_INTERFACES = '1.3.6.1.2.1.2.1.0'
GET_SYSTEM = '1.3.6.1.2.1.1.1.0'
MULTICAST_INT = '1.3.6.1.2.1.2.2.1.12.'

def getOid(hostname,version,comunidad,puerto):
    oids = []
    n_int = int(consulta(hostname,version,comunidad,puerto,NUMERO_DE_INTERFACES))
    for i in range(1,n_int+1):
        counter = int(consulta(hostname,version,comunidad,puerto,MULTICAST_INT+str(i)))
        if(counter!=0):
            oids.append(MULTICAST_INT+str(i))
    
    return oids[0]


OIDS = [
    '1.3.6.1.2.1.2.2.1.12.2',
    '1.3.6.1.2.1.4.9.0',
    '1.3.6.1.2.1.5.22.0',
    '1.3.6.1.2.1.6.11.0',
    '1.3.6.1.2.1.7.3.0'

]

class Monitor():

    def create(host):
        ret = rrdtool.create(f'{host}/{host}.rrd',
                            "--start",'N',
                            "--step",'60',
                            "DS:inmulticast:COUNTER:600:U:U",
                            "DS:inip:COUNTER:600:U:U",
                            "DS:icmpecho:COUNTER:600:U:U",
                            "DS:tcpsegsent:COUNTER:600:U:U",
                            "DS:udpin:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:6:5",
                            "RRA:AVERAGE:0.5:1:30")

        if ret:
            print (rrdtool.error())

    def graph(host, var, title, descr, t0 = str(int(time.time()) - 600), tf = 'N'):
        ret = rrdtool.graph(f'{host}/{host} {var}.png',
                        "--start",t0,
                        "--end",tf,
                        "--vertical-label=Bytes/s",
                        f"--title={title}",
                        f"DEF:{var}={host}/{host}.rrd:{var}:AVERAGE",
                        f"LINE3:{var}#0000FF:{descr}") 

    def Update(self):
        while(True):
            for host in self.host:
                o = getOid(host[0],host[1],host[2],host[3])
                OIDS[0] = o
                info = [getConsulta(host[0],host[1],host[2],host[3],oid) for oid in OIDS]
                info = 'N:' + ':'.join([str(e) for e in info])
                rrdtool.update(f'{host[0]}/{host[0]}.rrd', info)
                rrdtool.dump(f'{host[0]}/{host[0]}.rrd', f'{host[0]}/{host[0]}.xml')
                #print(info)


    def __init__(self,host):
        self.host = host
    
    
    def CrearRRD(self):
        for i in self.host:
            Monitor.create(i[0])

    def CrearCarpetas(self):
        for i in self.host:
            makedirs(i[0],exist_ok=True)

    def EliminarCarpeta(self):
        for i in self.host:
            rmdir(i[0])


'''if (__name__ == '__main__'):
    a = [['localhost',1,'comunidadASR',161],]
    m = Monitor(a)
    m.CrearCarpetas()
    m.CrearRRD()
    m.Update()'''