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
    loadEventos(catalog)
    loadGeneros(catalog)
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

def rango_caracteristica(catalog,caracteristica,rango_inf,rango_sup):
    return model.rango_caracteristica(catalog,caracteristica,rango_inf,rango_sup)

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
    model.new_genero(catalog,genero,rango_inf,rango_sup)

def total_por_generos(catalog,lista_gen):
    lista_gen2=lista_gen.split(',')
    return model.total_por_generos(catalog,lista_gen2)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup):
    return model.musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup)