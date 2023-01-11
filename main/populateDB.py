#encoding:utf-8
from main.models import Posicion, Division, Conferencia, Jugador, Equipo, Pais, SeasonLeaders

#encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request, re
from urllib.error import HTTPError
import time

#https://www.nba.com/teams
#https://www.hispanosnba.com/equipos

def populateDatabase():
    crearConferencias()
    crearPaises()
    creaDivisionesEquipos()
    crearPosiciones()
    crearJugadores()
    crearSeasonLeaders()
    return True

def creaDivisionesEquipos():
    #borrar tablas
    Division.objects.all().delete()
    Equipo.objects.all().delete()
    
    url = "https://www.nba.com/teams"
    file = urllib.request.urlopen(url)
    s = BeautifulSoup(file,"lxml")
    divisiones = s.find_all("div", class_="TeamDivisions_division__u3KUS")
    for division in divisiones:
        nombre = division.find("div", class_="TeamDivisions_divisionName__KFlSk").getText()
        new_division, created = Division.objects.get_or_create(name=nombre)
        if created:
            if not crearDivision(nombre):
                print("No se ha podido modificar la división: "+ nombre)
        equipos = division.find_all("div", class_="TeamFigure_tf__jA5HW")
        for equipo in equipos:
            team_name = equipo.a.getText()
            url_team = "https://www.nba.com" + equipo.find("div", class_="TeamFigure_tfLinks__gwWFj").a['href'][:-1]
            team_division = new_division
            este = ["Atlantic", "Central", "Southeast"]

            if team_division.name in este:
                team_conference = Conferencia.objects.get(name='Eastern')
            else:
                team_conference = Conferencia.objects.get(name='Western')

            url2 = "https://www.hispanosnba.com/equipos"
            file2 = urllib.request.urlopen(url2)
            s2 = BeautifulSoup(file2,"lxml")
            teams = s2.find("main", class_="content block").find_all("li")
            for team in teams:
                if team_name in team.a['title'] or team_name.split()[-1] in team.a['title']:
                    url_teaminfo = "https://www.hispanosnba.com" + team.a['href']
                    new_team, created = Equipo.objects.get_or_create(nombre=team_name)
                    if created:
                        if not crearEquipo(team_name, url_team, url_teaminfo, team_division, team_conference):
                            print("No se ha podido modificar el equipo: "+ team_name)
            print(new_team)

def crearConferencias():
    path = "data"
    Conferencia.objects.all().delete()

    lista=[]
    fileobj = open(path + '/conferencias.txt', 'r', encoding='utf-8')
    for line in fileobj.readlines():
        rip = str(line.strip()).split(',')
        lista.append(Conferencia(name=rip[0], nombre=rip[1], img=rip[2]))
    fileobj.close()
    Conferencia.objects.bulk_create(lista)

def crearPaises():
    path = "data"
    Pais.objects.all().delete()

    lista=[]
    fileobj = open(path + '/paises.txt', 'r', encoding='utf-8')
    for line in fileobj.readlines():
        rip = str(line.strip()).split(',')
        iso2 = rip[3]
        img = "https://flagcdn.com/16x12/"+ iso2.lower() +".png"
        pais = Pais(name=rip[1], nombre=rip[0], iso3=rip[4], bandera=img)
        lista.append(pais)
    fileobj.close()
    Pais.objects.bulk_create(lista)
    
def crearPosiciones():
    path = "data"
    Posicion.objects.all().delete()

    lista=[]
    fileobj = open(path + '/posiciones.txt', 'r', encoding='utf-8')
    for line in fileobj.readlines():
        rip = str(line.strip()).split(',')
        lista.append(Posicion(name=rip[0], nombre=rip[1]))
    fileobj.close()
    Posicion.objects.bulk_create(lista)
        
def crearJugadores():
    path = "data"
    Jugador.objects.all().delete()

    lista=[]
    fileobj = open(path + '/jugadores.txt', 'r', encoding='utf-8')
    for line in fileobj.readlines():
        rip = str(line.strip()).split(',')
        dorsal = rip[1]
        if dorsal == "":
            dorsal = None
        else:
            dorsal = int(rip[1])
            
        if rip[5]=="USA":
            pais = Pais.objects.get(iso3=rip[5])
        else:
            pais = Pais.objects.get(name=rip[5])
        
        jugador = Jugador(nombre=rip[0], dorsal=dorsal, edad=int(rip[2]), altura=rip[3], peso=rip[4], pais=pais, exp=int(rip[6]), equipo=Equipo.objects.get(nombre=rip[7]), imagen=rip[8], draft=rip[9], posicion=Posicion.objects.get(name=rip[10]))
        lista.append(jugador)
    fileobj.close()
    Jugador.objects.bulk_create(lista)

def crearDivision(name):
    traduce = {"Atlantic": "Atlántica", "Central": "Central", "Southeast": "Sudeste", "Northwest": "Noroeste", "Pacific": "Pacífica", "Southwest": "Suroeste"}
    este = ["Atlantic", "Central", "Southeast"]
    try:
        if name in este:
            conferencia = Conferencia.objects.get(name='Eastern')
        else:
            conferencia = Conferencia.objects.get(name='Western')
        Division.objects.filter(name=name).update(nombre=traduce[name], conferencia=conferencia)
    except:
        return False
    else:
        return True

def crearEquipo(team_name, url_team, url_teaminfo, team_division, team_conference):
    try:
        file = urllib.request.urlopen(url_teaminfo)
        s = BeautifulSoup(file,"lxml")
        info = s.find("div", class_="cuadro block").find_all("p")
        
        lugar = info[0].find("strong", string="Ciudad:").next_sibling[1:]
        estadio = info[2].a.getText()
        playoffs = int(info[8].find("strong", string="Presencias en playoff:").next_sibling[1:])
        campeonatos = int(info[5].find("strong", string="Títulos NBA:").next_sibling[1:])
        titulos_conferencia = int(info[6].find("strong", string="Títulos conferencia:").next_sibling[1:])
        titulos_division = int(info[7].find("strong", string="Títulos división:").next_sibling[1:])
        
        file2 = urllib.request.urlopen(url_team)
        regex_id = re.compile(r'(\d+)')
        team_id = int(regex_id.search(url_team).group(1))
        s2 = BeautifulSoup(file2,"lxml")
        escudo = "https://cdn.nba.com/logos/nba/"+str(team_id)+"/primary/L/logo.svg"
        wins = int(s2.find("div", class_="TeamHeader_record__wzofp").span.getText().split("-")[0])
        loses = int(s2.find("div", class_="TeamHeader_record__wzofp").span.getText().split("-")[1])

        Equipo.objects.filter(nombre=team_name).update(division=team_division, conferencia=Conferencia.objects.get(name=team_conference.name), lugar=lugar, playoffs=playoffs, campeonatos=campeonatos, titulos_conferencia=titulos_conferencia, titulos_division=titulos_division, escudo=escudo, estadio=estadio, url=url_team, wins=wins, loses=loses)
    except HTTPError as e: #Soluciona error 502 Bad Gateway
        if e.code == 502:
            time.sleep(1)
            crearEquipo(team_name, url_team, url_teaminfo, team_division, team_conference)
        else:
            print('Failure: ' + str(e.reason))
    else:
        return True;
    
def crearSeasonLeaders():
    SeasonLeaders.objects.all().delete()
    
    categorias = {"Points Per Game": "Puntos por partido", "Assists Per Game": "Asistencias por partido", "Rebounds Per Game": "Rebotes por partido", "Steals Per Game": "Robos por partido", "Blocks Per Game": "Tapones por partido", "Minutes Per Game": "Minutos por partido",}
    
    url = "https://www.nba.com/stats/players"
    file = urllib.request.urlopen(url)
    s = BeautifulSoup(file,"lxml")
    
    info = s.find_all("div", class_="LeaderBoardCard_leaderBoardCategory__vWRuZ")
    
    for i in range(0,5):
        category = info[i].a.getText()
        categoria = categorias[category]
        players = info[i].find("tbody").find_all("tr")
        for jugador in players:
            nombre = jugador.a.getText()
            jug = Jugador.objects.get(nombre=nombre)
            stat = float(jugador.find("td", class_="text-right").getText())
            SeasonLeaders.objects.create(category=category, categoria=categoria, lider=jug, stat=stat)
            
    #Rookies
    rookies = s.find("div", id="players_rookies").find("div", class_="LeaderBoardCard_leaderBoardCategory__vWRuZ")
    category = rookies.a.getText()
    categoria = categorias[category] + " (Rookies)"
    category = rookies.a.getText() + " (Rookies)"
    players = rookies.find("tbody").find_all("tr")
    for jugador in players:
        nombre = jugador.a.getText()
        jug = Jugador.objects.get(nombre=nombre)
        stat = float(jugador.find("td", class_="text-right").getText())
        SeasonLeaders.objects.create(category=category, categoria=categoria, lider=jug, stat=stat)
