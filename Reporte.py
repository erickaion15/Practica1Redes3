from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from consultaCompleta import *
w, h = A4
w = 740
h = 500


class Reporte:

    def __init__(self,a):
        self.hostname = a[0]
        self.version = a[1]
        self.comunidad = a[2]
        self.puerto = a[3]


    def CrearReporte(self):
        t = str(Consulta(self.hostname,self.version,self.comunidad,self.puerto,'1.3.6.1.2.1.1.1.0'))
        c = canvas.Canvas(f'{self.hostname}/{self.hostname}-Reporte.pdf')
        
        text = c.beginText(10,830)
        text.textLine(f"Administracion en Servicios de Red \n Practica1")
        c.drawText(text)
        text.textLine(f"Diaz Zamora Erick \n Boleta:2019630396 \n 4CM13")
        c.drawText(text)
        sistema = t[t.find('=')+1:]
        sistema = sistema.split(' ')
        imagen = 'Windows' if 'Windows' in sistema else 'Linux'
        t = t[t.find('=')+1:]
        c.drawImage(f'img/{imagen}.png', 500, 740, width = 100, height = 100)
        text.setFont("Times-Roman", 12)
        text.textLine(f"Descripcion:{t}")
        c.drawText(text)
        text = c.beginText(10,785)
        localizacion = str(Consulta(self.hostname,self.version,self.comunidad,self.puerto,'1.3.6.1.2.1.1.6.0'))
        localizacion = localizacion[localizacion.find('=')+1:]
        text.textLine(f'Localizacion:{localizacion}')
        c.drawText(text)
        text = c.beginText(10,770)
        n_int = str(Consulta(self.hostname,self.version,self.comunidad,self.puerto,'1.3.6.1.2.1.2.1.0'))
        n_int = n_int[n_int.find('=')+1:]
        text.textLine(f'Numero de Interfaces:{n_int}')
        c.drawText(text)
        text = c.beginText(10,755)
        tiempo = str(Consulta(self.hostname,self.version,self.comunidad,self.puerto,'1.3.6.1.2.1.1.3.0'))
        tiempo = tiempo[tiempo.find('=')+1:]
        tiempo = int(tiempo)/1
        text.textLine(f'Tiempo de actividad desde el último reinicio: {tiempo}')
        c.drawText(text)
        text = c.beginText(10,743)
        text.textLine(f'Comunidad: {self.comunidad}')
        c.drawText(text)
        text = c.beginText(10,730)
        text.textLine(f'Direcccion IP: {self.hostname}')
        c.drawText(text)
        text = c.beginText(10,710)
        text.textLine(f'Paquetes multicast que ha recibido una interfaz ')
        c.drawText(text)
        
        c.save()



if(__name__=='__main__'):
    r = Reporte('localhost')
    r.CrearReporte()