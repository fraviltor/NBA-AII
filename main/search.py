import os
import shutil

from main.models import Equipo, Jugador

from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser.default import MultifieldParser

index = "main/search_index"

def index_items():
    if os.path.exists(index):
        shutil.rmtree(index)
    os.mkdir(index)

    os.mkdir(os.path.join(index, "equipos"))
    equipos_indexados = index_equipos()

    os.mkdir(os.path.join(index, "jugadores"))
    jugadores_indexados = index_jugadores()

    return equipos_indexados, jugadores_indexados

def get_schema_jugador():
    return Schema(
        nombre=TEXT(stored=True),
        equipo=TEXT(stored=True),
        pais=TEXT(stored=True),
        posicion=TEXT(stored=True),
    )


def get_schema_equipo():
    return Schema(
        nombre=TEXT(stored=True),
        division=TEXT(stored=True),
        conferencia=TEXT(stored=True),
    )


def index_equipos():
    equipos = Equipo.objects.all()

    ix = create_in(index + "/equipos", schema=get_schema_equipo())
    writer = ix.writer()

    for equipo in equipos:
        writer.add_document(nombre=equipo.nombre,
                            division=equipo.division.nombre,
                            conferencia=equipo.division.conferencia.nombre)

    writer.commit()
    print("{} equipos indexados".format(ix.doc_count()))
    return ix.doc_count()

def index_jugadores():
    jugadores = Jugador.objects.all()

    ix = create_in(index + "/jugadores", schema=get_schema_jugador())
    writer = ix.writer()

    for jugador in jugadores:
        writer.add_document(nombre=jugador.nombre, 
                            equipo=jugador.equipo.nombre,
                            pais=jugador.pais.nombre,
                            posicion=jugador.posicion.nombre)
    writer.commit()
    print("{} jugadores indexados".format(ix.doc_count()))
    return ix.doc_count()

def busca_equipos(keywords):
    ix = open_dir(index + "/equipos")
    with ix.searcher() as searcher:
        print("Buscando equipos, keywords: {}".format(keywords))
        query = MultifieldParser(
            ["nombre", "division", "conferencia"], ix.schema).parse(str(keywords))
        results = searcher.search(query, limit=None)
        if(len(results) > 0):
            nombre_equipos = [r["nombre"] for r in results]
            return Equipo.objects.filter(nombre__in=nombre_equipos)
        else:
            return []

def busca_jugadores(keywords):
    ix = open_dir(index + "/jugadores")
    with ix.searcher() as searcher:
        print("Buscando jugadores, keywords: {}".format(keywords))
        query = MultifieldParser(
            ["nombre", "equipo", "pais", "posicion"], ix.schema).parse(str(keywords))
        results = searcher.search(query, limit=None)
        if(len(results) > 0):
            nombre_jugadores = [r["nombre"] for r in results]
            return Jugador.objects.filter(nombre__in=nombre_jugadores)
        else:
            return []