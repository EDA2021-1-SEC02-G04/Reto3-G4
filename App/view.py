"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import random

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

catalog = None

"""
Menu principal
"""
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de canciones")
    print("3- Caracterizar canciones")
    print("4- Encontrar musica para festejar")
    print("5- Encontrar musica para estudiar")
    print("6- Crear nuevo genero")
    print("7- Estimar las reproducciones de los generos musicales")
    print("8- Indicar el genero musical más escuchado en un tiempo")
    print("0- Salir")
    print("*******************************************")

def print_generos(respuesta):
    lista=respuesta[1]
    for res in lt.iterator(lista):
        print('\n======'+res[3]+'======')
        print('Para '+str(res[3])+' el rango esta entre '+str(res[4][0])+' y '+str(res[4][1]))
        print('Reproducciones totales de '+ str(res[3])+': '+str(res[0]))
        print('Numero total de artistas: '+str(res[2]))
        print('------Artistas de '+str(res[3])+'------')
        artistas=res[1]
        i=1
        while i <= 10 and i<=lt.size(artistas):
            print('Artista '+str(i)+': '+str(lt.getElement(artistas,i)))
            i+=1
def print_estudiar(respuesta):
    total=lt.size(respuesta)
    print('En total hay: '+str(total)+' pistas unicas con las caracteristicas ingresadas')
    print('------Pistas únicas------')
    i=1
    while i<=5 and i<=lt.size(respuesta):
        numero_pista=random.randint(1, lt.size(respuesta))
        pista=lt.getElement(respuesta,numero_pista)
        print('Pista '+str(i)+': '+ str(pista['track_id'])+' con instrumentalidad '+str(pista['instrumentalness'])+' y tempo '+str(pista['tempo']))
        i+=1
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de eventos de escucha ....")
        controller.loadData(catalog)
    elif int(inputs[0]) == 3:
        print("\nBuscando reprioducciónes por caracteristica: ")
        car = input("Ingrese la caracteristica de contenido: ").lower()
        rango_inf =float(input("Ingrese el limite inferior del rango de la caracteristica: "))
        rango_sup =float(input("Ingrese el limite superior del rango de la caracteristica: "))
        resultado= controller.rango_caracteristica(catalog,car,rango_inf,rango_sup)
        print('Numero de elementos: ' + str(resultado[0]))
        print('Altura del arbol: ' + str(resultado[1]))
        print('Numero de reproducciones:'+ str(resultado[2]))
        print('Cantidad de Autores:'+ str(resultado[3]))
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        print("\nBuscando musica para estudiar: ")
        inst_inf =float(input("Ingrese el limite inferior de Instrumentalness: "))
        inst_sup =float(input("Ingrese el limite superior de Instrumentalness: "))
        BPM_inf =float(input("Ingrese el limite inferior de BPM: "))
        BPM_sup =float(input("Ingrese el limite superior de BPM: "))
        answer=controller.musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup)
        print('La instrumentalidad está entre: ' +str(inst_inf)+' y '+str(inst_sup))
        print('El tempo está entre: ' +str(BPM_inf)+' y '+str(BPM_sup))
        print_estudiar(answer)
    elif int(inputs[0]) == 6:
        print("\nCreando nuevo genero: ")
        genero = input("Ingrese el nombre de su nuevo genero: ").lower()
        rango_inf =float(input("Ingrese el limite inferior de BPM: "))
        rango_sup =float(input("Ingrese el limite superior de BPM: "))
        controller.nuevo_genero(catalog,genero,rango_inf,rango_sup)
        print("Se creó su nuevo genero")
    elif int(inputs[0]) == 7:
        print("\nBuscando por genero: ")
        generos = input("Ingrese los generos separados por ,: ").lower()
        resultado=controller.total_por_generos(catalog,generos)
        print("Total de reproducciónes:" +str(resultado[0]))
        print_generos(resultado)
    elif int(inputs[0]) == 8:
        pass
    else:
        sys.exit(0)
sys.exit(0)