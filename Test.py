import sys
import rrdtool
import time

def graph(filename, var, title, descr, t0 = 'N', tf = 'N'):
    ret = rrdtool.graph(f'{filename}/{filename} {var}.png',
                     "--start",t0,
                     "--end",tf,
                     "--vertical-label=Bytes/s",
                     f"--title={title}",
                     f"DEF:{var}={filename}/{filename}.rrd:{var}:AVERAGE",
                     f"LINE3:{var}#0000FF:{descr}")




t0 = str(int(time.time()) - 600)
graph('localhost','inunicast','Paquetes unicast recibidos', 'Paquetes', t0, 'N')
graph('localhost', 'inip', 'Paquetes IPV4 recibidos', 'Paquetes', t0, 'N')
graph('localhost', 'icmpecho', 'Mensajes ICMP echo enviados', 'Mensajes', t0, 'N')
graph('localhost', 'tcpsegsin', 'Segmentos TCP recibidos', 'Segmentos', t0, 'N')
graph('localhost', 'udpindtgr', 'Datagramas UDP entregados', 'Datagramas', t0, 'N')