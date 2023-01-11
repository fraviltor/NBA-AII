#encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request, re

import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

#Necesario para solucionar error 502 Bad Gateway

def jugadoresEquipo_alt(team, url_team):
    file = urllib.request.urlopen(url_team)
    s = BeautifulSoup(file,"lxml")
    jugadores = s.find("table").find_all("td", class_="primary text")
    for jugador in jugadores:
        nombre = jugador.a.getText()
        #regex_id = re.compile(r'(\d+)')
        #id = int(regex_id.search(jugador.a['href'][:-1]).group(1))
        #url = "https://www.nba.com/stats/player/" + str(id)
        url = "https://www.nba.com" + jugador.a['href'][:-1]
        print(nombre)
        file2 = urllib.request.urlopen(url)
        s2 = BeautifulSoup(file2,"lxml")
        main_info = s2.find("p", class_="PlayerSummary_mainInnerInfo__jv3LO").string.replace(" ", "").split("|")
        if "#" in main_info[1]:
            dorsal = int(main_info[1].replace("#",""))
            posicion = main_info[2]
        else:
            dorsal=""
            posicion = main_info[1]
        
        info = s2.find_all("p", class_="PlayerSummary_playerInfoValue__JS8_v")
        regex_parentesis = re.compile(r'\((.+?)\)')
        regex_edad = re.compile(r'(\d+)')
        altura = regex_parentesis.search(info[0].getText()).group(1)
        peso = regex_parentesis.search(info[1].getText()).group(1)
        pais = info[2].getText()
        edad = int(regex_edad.search(info[4].getText()).group(1))
        exp = info[7].getText()
        if exp == "Rookie":
            exp = 0
        else:
            exp = int(regex_edad.search(exp).group(1))
        draft = info[6].getText()
        
        img = s2.find("img", class_="PlayerImage_image__wH_YX")['src']

        fileobj = open("data/jugadores.txt", "a")
        fileobj.write(str(nombre)+","+str(dorsal)+","+str(edad)+","+str(altura)+","+str(peso)+","+str(pais)+","+str(exp)+","+str(team)+","+str(img)+","+str(draft)+","+str(posicion) + "\n")
        fileobj.close()

def crearTxtJugadores():
    teams = [] #Manualmente para evitar error 502 Bad Gateway
    urls_team = [] #Manualmente para evitar error 502 Bad Gateway
    dicc = dict(zip(teams, urls_team))
    for team in dicc:
        jugadoresEquipo_alt(team, dicc[team])
        
def crearTxtPosiciones():
    dicc = {"Guard": "Base", "Guard-Forward":"Base-Escolta",  "Forward": "Alero", "Forward-Guard": "Alero-Escolta", "Forward-Center": "Alero-Ala Pivot", "Center": "Pivot", "Center-Forward": "Pivot-Ala Pivot"}
    conjunto = set()
    fileread = open("data/jugadores.txt", "r")
    for line in fileread.readlines():
        rip = str(line.strip()).split(',')
        posicion = rip[10]
        conjunto.add(posicion)
        
    fileobj = open("data/posiciones.txt", "a")
    for valor in conjunto:
        fileobj.write(str(valor) + "," + dicc[str(valor)] + "\n")
    fileobj.close()
        
#crearTxtJugadores()
#crearTxtPosiciones()