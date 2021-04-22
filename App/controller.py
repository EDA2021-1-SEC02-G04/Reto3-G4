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
 """

import config as cf
import model
import csv


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

def loadEventos(catalog):
    eventosfile = cf.data_dir + 'context_content_features-small.csv'
    input_file = csv.DictReader(open(eventosfile, encoding='utf-8'))
    for evento in input_file:
        model.addEvento(catalog,evento)

def rango_caracteristica(catalog,caracteristica,rango):
    return model.rango_caracteristica(catalog,caracteristica,rango)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
