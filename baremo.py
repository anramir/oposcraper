import mechanize
from bs4 import BeautifulSoup
url='http://www.juntadeandalucia.es/educacion/nav/navegacion.jsp?pagActual=3&lista_canales=6&mes_filtro=6&vismenu='
br=mechanize.Browser()
br.open(url)
links=br.links()
for link in links:
    if 'BAREMO' in link.text:
        enlace=link
br.follow_link(enlace)
br.select_form("NDNI")
br.form['DNI']=''
page=br.submit()
html=page.read()
soup=BeautifulSoup(html)
elementos=soup.find_all('td')
print float(elementos[-3].text[-6:])


