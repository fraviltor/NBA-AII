from django.shortcuts import render, get_object_or_404
from main.models import Posicion, Division, Jugador, Equipo, Pais, Conferencia, SeasonLeaders
from main.populateDB import populateDatabase
from main.search import index_items, busca_jugadores, busca_equipos
from main.forms import PlayerBusquedaForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    divisiones = Division.objects.all()
    equipos = Equipo.objects.all()
    conferencias = Conferencia.objects.all()
    divs = ['Atlantic', "Central", "Southeast","Northwest", "Pacific", "Southwest"]
    dicc = dict()
    
    for div in divisiones:
        nombre = div.nombre
        lista = []
        for e in equipos:
            division = e.division.nombre
            if division == nombre:
                lista.append(e)
        dicc[div]= lista
        
    informacion="Actualmente tenemos almacenadas:\n" + str(Division.objects.count())+ " divisiones " + " , " + str(Equipo.objects.count()) + " equipos " + " y " + str(Jugador.objects.count())+ " jugadores." 
        
    return render(request,'index.html', {'title':"Inicio", 'inf':informacion, 'dicc':dicc, 'conferencias':conferencias, 'divisiones':divs})

def cargar(request):
    if populateDatabase():
        divisiones = Division.objects.all().count()
        equipos = Equipo.objects.all().count()
        paises = Pais.objects.count()
        jugadores = Jugador.objects.count()
        posiciones = Posicion.objects.count()
        informacion="Datos cargados correctamente\n" + "Divisiones: " + str(divisiones)+ " ; " + "Equipos: " + str(equipos) + " ; " + "Jugadores: " + str(jugadores) + " ; " + "Paises: " + str(paises) + " ; " + "Posiciones: " + str(posiciones)
    else:
        informacion="ERROR en la carga de datos"    
    return render(request, 'carga.html', {'title':"Carga", 'inf':informacion})

def indexItems(request):
    indexed_teams, indexed_players = index_items()
    return render(request, 'indexed.html', {"title":"Indexado", "indexed_teams": indexed_teams, "indexed_players": indexed_players})

def clasificacion(request):
    equipos = Equipo.objects.all().order_by('-wins')
    conferencias = Conferencia.objects.all()
    oeste = Equipo.objects.filter(conferencia=Conferencia.objects.get(name="Western")).order_by('-wins')
    este = Equipo.objects.filter(conferencia=Conferencia.objects.get(name="Eastern")).order_by('-wins')
    return render(request,'clasificacion.html',{'title':"Clasificaciones",'equipos':equipos, 'conferencias':conferencias, 'este':este, 'oeste':oeste})

def lideres(request):
    lideres = SeasonLeaders.objects.all()
    categorias = set()
    res = dict()
    for lider in lideres:
        cat = lider.categoria
        categorias.add(cat)

    for categ in sorted(categorias):
        lideres_esa_categoria = []
        for lider in lideres:
            if lider.categoria == categ:
                lideres_esa_categoria.append((lider.lider,lider.stat))
        res[categ]=lideres_esa_categoria
        
    return render(request,'lideres.html',{'title':"Líderes", 'res':res})

def vista_equipo(request, id_equipo):
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    plantilla = Jugador.objects.filter(equipo=equipo).order_by('dorsal')
    return render(request,'vista_equipo.html',{'equipo':equipo, 'plantilla':plantilla})

def vista_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    return render(request,'vista_jugador.html',{'jugador':jugador})

def busca(request):
    keyword = "' ' "
    
    if request.POST or request.session.get('initial_for_form', None) is not None:
        if request.POST:
            data = request.POST
        else:
            data = request.session.get('initial_for_form')
    
        form = PlayerBusquedaForm(data)
        if form.is_valid():
            keyword=form.cleaned_data['player_name']
            jugadores = busca_jugadores(keyword)
            equipos = busca_equipos(keyword)
            results = []
            
            for e in equipos:
                results.append(e)
            for j in jugadores:
                results.append(j)
            
            paginator = Paginator(results, 5)
            page = request.GET.get('page')
        
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            # escribes la sesion con los datos del formulario
            request.session['initial_for_form'] = form.cleaned_data

            return render(request,'buscador.html',{'title':"Buscador",'results':results, 'keyword':keyword})#, 'equipos':equipos})
    
    return render(request, 'buscador.html', {'title':"Buscador",'keyword':keyword})
