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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo 

def init():
    catalog = model.newCatalog()
    model.anadir_caracteristicas(catalog)
    model.crear_arboles(catalog)
    return catalog
# Funciones para la carga de datos
def loadData(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadEventos(catalog)
    loadGeneros(catalog)
    loadHashtag(catalog)
    model.llenar_arboles(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    print(mp.size(catalog['eventos']))

def loadEventos(catalog):
    eventosfile = cf.data_dir + 'context_content_features-small.csv'
    input_file_eventos = csv.DictReader(open(eventosfile, encoding='utf-8'))
    for evento in input_file_eventos:
        model.addEvento(catalog,evento)
    hastagfile = cf.data_dir + 'user_track_hashtag_timestamp-small.csv'
    input_file_hashtag = csv.DictReader(open(hastagfile, encoding='utf-8'))
    for evento in input_file_hashtag:
        model.hastags(catalog,evento)
def loadHashtag(catalog):
    hashtagfile = cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(hashtagfile, encoding='utf-8'))
    for hashtag in input_file:
        model.poner_vader(catalog,hashtag)

def rango_caracteristica(catalog,caracteristica,rango_inf,rango_sup):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta= model.rango_caracteristica(catalog,caracteristica,rango_inf,rango_sup)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return respuesta

def loadGeneros(catalog):
    model.new_genero(catalog,'reggae',60,90)
    model.new_genero(catalog,'down-tempo',70,100)
    model.new_genero(catalog,'chill-out',90,120)
    model.new_genero(catalog,'hip-hop',85,115)
    model.new_genero(catalog,'jazz and funk',120,125)
    model.new_genero(catalog,'pop',100,130)
    model.new_genero(catalog,'r&b',60,80)
    model.new_genero(catalog,'rock',110,140)
    model.new_genero(catalog,'metal',100,160)

def nuevo_genero(catalog,genero,rango_inf,rango_sup):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    model.new_genero(catalog,genero,rango_inf,rango_sup)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

def total_por_generos(catalog,lista_gen):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lista_gen2=lista_gen.split(',')
    respuesta=model.total_por_generos(catalog,lista_gen2)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return respuesta

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return respuesta

def musica_festejar(catalog,dance_inf,dance_sup,temp_inf,temp_sup):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.musica_festejar(catalog,dance_inf,dance_sup,temp_inf,temp_sup)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return respuesta

def analisis_por_hora(catalog,tmin,tmax):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta=model.analisis_por_hora(catalog,tmin,tmax)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return respuesta

# Funciones de tiempo y memoria

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
