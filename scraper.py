import mechanize
from pymongo import MongoClient
from bs4 import BeautifulSoup
import json
import sys, os
reload(sys)
import time
sys.setdefaultencoding('utf-8')
import subprocess
from opositor import Opositor
subprocess.Popen(['C:\\Program Files\\MongoDB\\server\\3.0\\bin\\mongod','--dbpath','D:\\data\\db','--port','27017'])

client = MongoClient()
client = MongoClient('localhost', 27017)

db=client.oposiciones
basedatos=db['opositores']
url = 'http://www.juntadeandalucia.es/educacion/nav/navegacion.jsp?pagActual=4&lista_canales=6&mes_filtro=6&vismenu='

br=mechanize.Browser()
br.open(url)
links=br.links()
for link in links:
    if 'ConsNotas' in link.url:
        enlace=link
br.follow_link(enlace)
for i in range(25):
    br.select_form('globe')
    br.form['Espec']=['036']
    br.submit()
    br.select_form(nr=i)
    page=br.submit()
    html=page.read()
    soup=BeautifulSoup(html)
    tribunal=soup.find_all('font')
    provincia=tribunal[0].text.split('(')[2].split(')')[0]
    opositores=soup.find_all('tr')
    for opositor in opositores:
        datos=opositor.find_all('td')
        try:
            apellidos=datos[2].text.split(' , ')[0]
            nombre=datos[2].text.split(' , ')[1]
            persona=Opositor(datos[0].text,datos[1].text,apellidos,nombre)
            persona.setNotas(datos[4].text,datos[5].text,datos[6].text,datos[7].text,datos[8].text,datos[9].text,datos[10].text,i+1,provincia)
            basedatos.insert_one(persona.parametros).inserted_id
        except:
            print 'error'
    links=br.links()
    for link in links:
        if link.text=="Nueva consulta":
            br.follow_link(link)