﻿"""
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
import datetime
assert cf


# Construccion de modelos
def newCatalog():
    catalog = {'eventos': None,
                'caracteristicas_de_contenido':None,
                'index_caracteristica': None,
                'genero-rango':None,
                'vader_promedio':None
                }

    catalog['eventos'] = mp.newMap(100000,maptype="PROBING",loadfactor=0.5)
    catalog['caracteristicas_de_contenido'] = lt.newList(datastructure='SINGLE_LINKED')
    catalog['index_caracteristica'] = mp.newMap(20,maptype="PROBING",loadfactor=0.5)
    catalog["genero-rango"]=mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    catalog["vader_promedio"]=mp.newMap(10000,maptype="PROBING",loadfactor=0.5)
    return catalog
# Funciones para agregar informacion al catalogo


def anadir_caracteristicas(catalog):
    lista=catalog['caracteristicas_de_contenido']
    caracteristicas="instrumentalness,liveness,speechiness,danceability,valence,loudness,tempo,acousticness,energy,mode,key,created_at"
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
    tiempo=datetime.datetime.strptime(evento['created_at'], '%Y-%m-%d %H:%M:%S')
    tupla=(evento['track_id'],evento['user_id'],tiempo)
    evento['created_at']=tiempo
    evento['hashtag']=lt.newList(datastructure='SINGLE_LINKED')
    if mp.contains(catalog['eventos'], tupla):
        pass
    else:
        mp.put(catalog['eventos'],tupla, evento)
    return catalog

def hastags(catalog,evento):
    tiempo=datetime.datetime.strptime(evento['created_at'], '%Y-%m-%d %H:%M:%S')
    tupla=(evento['track_id'],evento['user_id'],tiempo)
    evento['created_at']=tiempo
    if mp.contains(catalog['eventos'], tupla):
        aguacate=mp.get(catalog['eventos'], tupla)
        evento_map=me.getValue(aguacate)
        lt.addLast(evento_map['hashtag'], evento['hashtag'])
        mp.remove(catalog['eventos'], tupla),
        mp.put(catalog['eventos'], tupla, evento_map)
    else:
        hashtag=evento['hashtag']
        evento['hashtag']=lt.newList(datastructure='SINGLE_LINKED')
        lt.addLast(evento['hashtag'], hashtag)
        mp.put(catalog['eventos'],tupla, evento)
    return catalog

def llenar_arboles(catalog):
    valores=mp.valueSet(catalog['eventos'])
    for evento in lt.iterator(valores):
        llenar_mapas(catalog,evento)
    return catalog

def llenar_mapas(catalog,evento):
    mapa=catalog['index_caracteristica']
    for caracteristica in lt.iterator(catalog['caracteristicas_de_contenido']):
        caracteristica=caracteristica.strip('"')
        x=mp.get(mapa,caracteristica)
        valor=me.getValue(x)
        if evento.get(caracteristica) != None:
            if caracteristica=='created_at':
                tiempo=evento['created_at']
                hora=tiempo.time()
                om.put(valor, hora, evento)
            else:             
                om.put(valor, float(evento[caracteristica]), evento)
    return catalog

def llenar_mapa_tempo(lista):
    arbol=om.newMap(omaptype='RBT',comparefunction=compare_car)
    for evento in lt.iterator(lista):
        if evento.get('tempo') != None:
            om.put(arbol,float(evento['tempo']), evento)
    return arbol

def poner_vader(catalog,hashtag):
    mp.put(catalog['vader_promedio'],hashtag['hashtag'],hashtag['vader_avg'])

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

def pistas_unicas(lista):
    map_pistas=mp.newMap(numelements=2*lt.size(lista),maptype='PROBING',loadfactor=0.5)
    for evento in lt.iterator(lista):
        tupla=(evento['track_id'],evento['user_id'],evento['created_at'])
        if mp.contains(map_pistas,tupla):
            None
        else:
            mp.put(map_pistas,tupla,evento)
    return map_pistas

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

def musica_festejar(catalog,dance_inf,dance_sup,temp_inf,temp_sup):
    map_dance=mp.get(catalog['index_caracteristica'],'danceability')
    map_temp=mp.get(catalog['index_caracteristica'],'energy')
    arbol_dance=me.getValue(map_dance)
    arbol_temp=me.getValue(map_temp)
    valores_dance=om.values(arbol_dance,dance_inf,dance_sup)
    valores_temp=om.values(arbol_temp,temp_inf,temp_sup)
    mapa_dance=lista_en_hash(valores_dance)
    lista_musica=lt.newList('ARRAY_LIST')
    for evento in lt.iterator(valores_temp):
        if mp.contains(mapa_dance,evento['track_id']):
            lt.addLast(lista_musica,evento)
    lista_unica=mp.valueSet(pistas_unicas(lista_musica))
    return lista_unica

def musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup):
    map_inst=mp.get(catalog['index_caracteristica'],'instrumentalness')
    map_BPM=mp.get(catalog['index_caracteristica'],'tempo')
    arbol_inst=me.getValue(map_inst)
    arbol_BPM=me.getValue(map_BPM)
    valores_inst=om.values(arbol_inst,inst_inf,inst_sup)
    valores_BPM=om.values(arbol_BPM,BPM_inf,BPM_sup)
    mapa_inst=lista_en_hash(valores_inst)
    lista_musica=lt.newList('ARRAY_LIST')
    for evento in lt.iterator(valores_BPM):
        if mp.contains(mapa_inst,evento['track_id']):
            lt.addLast(lista_musica,evento)
    lista_unica=mp.valueSet(pistas_unicas(lista_musica))
    return lista_unica

def lista_en_hash(lista):
    mapa=mp.newMap(2*lt.size(lista),maptype="PROBING",loadfactor=0.5)
    for evento in lt.iterator(lista):
        mp.put(mapa,evento['track_id'],evento)
    return mapa

def promedio_vader(catalog,lista):
    for evento in lt.iterator(lista):
        total=0
        for hashtag in lt.iterator(evento['hashtag']):
            pareja=mp.get(catalog['vader_promedio'], hashtag)
            if pareja != None:
                vader=me.getValue(pareja)
                if vader!= '':
                    total+=float(vader)
        promedio=total/lt.size(evento['hashtag'])
        evento['vader']=promedio
    return lista

def analisis_por_hora(catalog,tmin,tmax):
    mindate=datetime.datetime.strptime(tmin, '%H:%M:%S')
    maxdate=datetime.datetime.strptime(tmax, '%H:%M:%S')
    mintime=mindate.time()
    maxtime=maxdate.time()
    map_hora=mp.get(catalog['index_caracteristica'],'created_at')
    arbol_hora=me.getValue(map_hora)
    eventos_rango=om.values(arbol_hora, mintime, maxtime)
    total_rep=lt.size(eventos_rango)
    arbol=llenar_mapa_tempo(eventos_rango)
    genero_mas=None
    genero_nombre=None
    tamaño_genero=0
    lista_generos=lt.newList(datastructure='ARRAY_LIST')
    for genero in lt.iterator(mp.keySet(catalog['genero-rango'])):
        rango=cambiar_genero_rango(catalog,genero)
        valores_rango=om.values(arbol,float(rango[0]),float(rango[1]))
        total=lt.size(valores_rango)
        tupla=(genero,valores_rango,total)
        lt.addLast(lista_generos, tupla)
    ordenada_por_genero=sa.sort(lista_generos, cmpgeneros)
    genero_mas=lt.getElement(ordenada_por_genero, 1)
    promedio=promedio_vader(catalog,genero_mas[1])
    lista_unica=mp.valueSet(pistas_unicas(promedio))
    ordenada_hashtag=sa.sort(lista_unica, cmphashtags)
    return (ordenada_por_genero,genero_mas,promedio,ordenada_hashtag,total_rep)

    
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compare_car(car1, car2):
    if (car1 == car2):
        return 0
    elif (car1 > car2):
        return 1
    else:
        return -1

def cmpgeneros(gen1, gen2):
    
    if (gen1[2] > gen2[2]):
        return True
    else:
        return False

def cmphashtags(ev1, ev2):
    
    if (lt.size(ev1['hashtag']) > lt.size(ev2['hashtag'])):
        return True
    else:
        return False