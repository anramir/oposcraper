import mechanize
from bs4 import BeautifulSoup


class Opositor:
    def __init__(self,naspirante,nif,apellidos,nombre):
        self.parametros={}
        self.parametros['naspirante']=naspirante
        self.parametros['nif']=nif
        self.parametros['apellidos']=apellidos
        self.parametros['nombre']=nombre


    def setNotas(self,prueba1,ppractica,tema,prueba2,pdidactica,udidactica,noposicion,ntribunal,provincia):
        self.parametros['prueba1']=self.checker(prueba1)
        self.parametros['ppractica']=self.checker(ppractica)
        self.parametros['tema']=self.checker(tema)
        self.parametros['prueba2']=self.checker(prueba2)
        self.parametros['pdidactica']=self.checker(pdidactica)
        self.parametros['udidactica']=self.checker(udidactica)
        self.parametros['noposicion']=self.checker(noposicion)
        self.parametros['tribunal']={}
        self.parametros['tribunal']['ntribunal']=ntribunal
        self.parametros['tribunal']['provincia']=provincia
        if self.parametros['noposicion']>0:
            self.parametros['baremo']=self.checkBaremo(self.parametros['nif'])
        print self.parametros

    def setNotasPrueba1(self, prueba1, ppractica, tema, ntribunal, provincia):
        self.parametros['prueba1']=self.checker(prueba1)
        self.parametros['ppractica']=self.checker(ppractica)
        self.parametros['tema']=self.checker(tema)
        self.parametros['tribunal']={}
        self.parametros['tribunal']['ntribunal']=ntribunal
        self.parametros['tribunal']['provincia']=provincia

    def checker(self,parametro):
        if '---no---' in parametro:
            resultado=-1
        else:
            resultado=float(parametro[-6:])
        return resultado

    def checkBaremo(self,dni):
        url='http://www.juntadeandalucia.es/educacion/nav/navegacion.jsp?pagActual=3&lista_canales=6&mes_filtro=6&vismenu='
        br=mechanize.Browser()
        br.open(url)
        links=br.links()
        for link in links:
            if 'BAREMO' in link.text:
                enlace=link
        br.follow_link(enlace)
        br.select_form("NDNI")
        br.form['DNI']=dni
        page=br.submit()
        html=page.read()
        soup=BeautifulSoup(html)
        elementos=soup.find_all('td')
        return float(elementos[-3].text[-6:])
