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
                'index_caracteristica': None
                }

    catalog['eventos'] = lt.newList('SINGLE_LINKED')
    catalog['caracteristicas_de_contenido'] = lt.newList('SINGLE_LINKED')
    catalog['index_caracteristica'] = mp.newMap(20,maptype="PROBING",loadfactor=0.5)
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
        arbol=om.newMap(omaptype='BST',comparefunction=compare_car)
        mp.put(mapa,caracteristica,arbol)

def addEvento(catalog,evento):
    
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compare_car(car1, car2):
    """
    Compara dos fechas
    """
    if (car1 == car2):
        return 0
    elif (car1 > car2):
        return 1
    else:
        return -1
