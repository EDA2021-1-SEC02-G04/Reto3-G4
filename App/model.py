"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'eventos': None,
                'caracteristicas_de_contenido':None,
                'index_caracteristica': None,
                'genero-rango':None
                }

    catalog['eventos'] = lt.newList('SINGLE_LINKED')
    catalog['caracteristicas_de_contenido'] = lt.newList('SINGLE_LINKED')
    catalog['index_caracteristica'] = mp.newMap(20,maptype="PROBING",loadfactor=0.5)
    catalog["genero-rango"]=mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    return catalog
# Funciones para agregar informacion al catalogo


def anadir_caracteristicas(catalog):
    lista=catalog['caracteristicas_de_contenido']
    caracteristicas="instrumentalness,liveness,speechiness,danceability,valence,loudness,tempo,acousticness,energy,mode,key"
    lista_car=caracteristicas.split(',')
    for caracteristica in lista_car:
        lt.addLast(lista,caracteristica)


def crear_arboles(catalog):
    car_lista=catalog['caracteristicas_de_contenido']
    mapa=catalog['index_caracteristica']
    for caracteristica in lt.iterator(car_lista):
        arbol=om.newMap(omaptype='RBT',comparefunction=compare_car)
        mp.put(mapa,caracteristica,arbol)

def addEvento(catalog,evento):
    lt.addLast(catalog['eventos'], evento)
    llenar_mapas(catalog, evento)
    return catalog


def llenar_mapas(catalog,evento):
    mapa=catalog['index_caracteristica']
    for caracteristica in lt.iterator(catalog['caracteristicas_de_contenido']):
        caracteristica=caracteristica.strip('"')
        x=mp.get(mapa,caracteristica)
        valor=me.getValue(x)
        om.put(valor, float(evento[caracteristica]), evento)
    return catalog

def llenar_mapa(catalog,caracteristica):
    for evento in lt.iterator(catalog['eventos']):
        mapa=catalog['index_caracteristica']
        caracteristica=caracteristica.strip('"')
        x=mp.get(mapa,caracteristica)
        valor=me.getValue(x)
        om.put(valor, float(evento[caracteristica]), evento)
    return catalog

def rango_caracteristica(catalog,caracteristica,rango_inf,rango_sup):
    map=mp.get(catalog['index_caracteristica'],caracteristica)
    arbol=me.getValue(map)
    valores_rango=om.values(arbol,rango_inf,rango_sup)
    cantidad_eventos=lt.size(valores_rango)
    lista_autores=autores_unicos(valores_rango)
    autores=lt.size(lista_autores)
    tamaño=om.size(arbol)
    altura=om.height(arbol)
    return(tamaño,altura,cantidad_eventos,autores)

def autores_unicos(lista):
    map_autores=mp.newMap(numelements=5000,maptype='PROBING',loadfactor=0.5)
    for evento in lt.iterator(lista):
        if mp.contains(map_autores,evento['artist_id']):
            None
        else:
            mp.put(map_autores,evento['artist_id'],evento['artist_id'])
    return map_autores
# Funciones para creacion de datos
def cambiar_genero_rango(catalog,genero):
    x=mp.get(catalog['genero-rango'],genero)
    return me.getValue(x)

def new_genero(catalog,genero,rango_inf,rango_sup):
    rango=(rango_inf,rango_sup)
    mp.put(catalog['genero-rango'],genero,rango)
# Funciones de consulta
def buscar_por_genero(catalog,genero):
    rango=cambiar_genero_rango(catalog,genero)
    map=mp.get(catalog['index_caracteristica'],'tempo')
    arbol=me.getValue(map)
    valores_rango=om.values(arbol,float(rango[0]),float(rango[1]))
    total=lt.size(valores_rango)
    artistas=mp.keySet(autores_unicos(valores_rango))
    numero_artistas=lt.size(artistas)
    return(total,artistas,numero_artistas,genero,rango)

def total_por_generos(catalog,lista_gen):
    total=0
    ltrespuesta=lt.newList(datastructure='ARRAY_LIST')
    for genero in lista_gen:
        respuesta=buscar_por_genero(catalog,genero)
        total+=respuesta[0]
        lt.addLast(ltrespuesta,respuesta)
    return (total,ltrespuesta)

def musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup):
    map_inst=mp.get(catalog['index_caracteristica'],'instrumentalness')
    map_BPM=mp.get(catalog['index_caracteristica'],'tempo')
    arbol_inst=me.getValue(map_inst)
    arbol_BPM=me.getValue(map_BPM)
    valores_inst=om.values(arbol_inst,inst_inf,inst_sup)
    valores_BPM=om.values(arbol_BPM,BPM_inf,BPM_sup)
    map_inst=lista_en_hash(valores_inst)
    lista_musica=lt.newList('ARRAY_LIST')
    for evento in lt.iterator(valores_BPM):
        if mp.contains(map_inst,evento):
            lt.addLast(lista_musica,evento)
    return lista_musica

def lista_en_hash(lista):
    mapa=mp.newMap(2*lt.size(lista),maptype="PROBING",loadfactor=0.5)
    for evento in lt.iterator(lista):
        mp.put(mapa,evento['track_id'],evento)
    return map
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compare_car(car1, car2):
    if (car1 == car2):
        return 0
    elif (car1 > car2):
        return 1
    else:
        return -1
