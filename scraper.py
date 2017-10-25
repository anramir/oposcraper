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
subprocess.Popen(['C:\\Program Files\\MongoDB\\Server\\3.4\\bin\\mongod','--dbpath','D:\\data\\db','--port','27017'])

client = MongoClient()
client = MongoClient('localhost', 27017)



URL = 'http://www.juntadeandalucia.es/educacion/portals/web/ced/novedades'
URL_NOTAS = 'http://www.juntadeandalucia.es/educacion/vscripts/dgprh/Oposiciones/L177/ConsNotas.asp'
ESPECIALIDAD = '037'
NUMERO_TRIBUNALES = 13
NOMBRE_BASE = 'al'

db=client[NOMBRE_BASE]
basedatos=db['opositores']

br = mechanize.Browser()
br.open(URL)

for link in br.links():
    if link.url == URL_NOTAS:
        notas_link = link

br.follow_link(notas_link)

for i in range(NUMERO_TRIBUNALES):
    br.select_form('globe')
    br.form['Espec']=[ESPECIALIDAD]
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
            # persona.setNotas(datos[4].text,datos[5].text,datos[6].text,datos[7].text,datos[8].text,datos[9].text,datos[10].text,i+1,provincia)
            persona.setNotasPrueba1(datos[4].text,datos[5].text,datos[6].text,i+1,provincia)
            print persona.parametros
            basedatos.insert_one(persona.parametros).inserted_id
        except:
            print 'error'
    links=br.links()
    for link in links:
        if link.text=="Nueva consulta":
            br.follow_link(link)