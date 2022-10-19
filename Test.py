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
