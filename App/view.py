﻿"""
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
    print("1- Inicializar catalogo")
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

def print_fiesta(respuesta):
    total=lt.size(respuesta)
    print('En total hay: '+str(total)+' pistas unicas con las caracteristicas ingresadas')
    print('------Pistas únicas------')
    i=1
    while i<=5 and i<=lt.size(respuesta):
        numero_pista=random.randint(1, lt.size(respuesta))
        pista=lt.getElement(respuesta,numero_pista)
        print('Pista '+str(i)+': '+ str(pista['track_id'])+' con Energy '+str(pista['energy'])+' y Danceability '+str(pista['danceability']))
        i+=1

def print_horas(respuesta,tmin,tmax):
    print('En total hay: '+str(respuesta[4])+' reproducciones entre '+str(tmin)+' y '+str(tmax))
    print('\n============ GENEROS SORTEADOS POR REPRODUCCIONES ============')
    i=1
    for genero in lt.iterator(respuesta[0]):
        print('TOP '+ str(i)+':'+ str(genero[0])+' con '+ str(genero[2])+' reproducciones')
        i+=1
    print('El genero más escuchado es: '+ str(respuesta[1][0]) +' con '+ str(respuesta[1][2])+ ' reproducciones')
    print('\n============ ANALISIS DE SENTIMIENTOS DE ' + str(respuesta[1][0]) + ' ============')
    print(str(respuesta[1][0])+' tiene '+ str(lt.size(respuesta[3]))+ ' tracks unicos')
    print('Los primeros 10 tracks son:')
    tracks=respuesta[3]
    j=1
    while j <= 10 and i<=lt.size(respuesta[3]):
        print('TOP '+ str(j)+' track:'+ str(lt.getElement(tracks, j)['track_id'])+ ' con '+ str(lt.size(lt.getElement(tracks, j)['hashtag'])) + ' hashtags y VADER '+str(lt.getElement(tracks, j)['vader']))
        j+=1
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
        answer=controller.loadData(catalog)
        print('Eventos cargados: ' + str(lt.size(catalog['eventos'])))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 3:
        print("\nBuscando reprioducciónes por caracteristica: ")
        car = input("Ingrese la caracteristica de contenido: ").lower()
        rango_inf =float(input("Ingrese el limite inferior del rango de la caracteristica: "))
        rango_sup =float(input("Ingrese el limite superior del rango de la caracteristica: "))
        resultado= controller.rango_caracteristica(catalog,car,rango_inf,rango_sup)
        print('Numero de reproducciones:'+ str(resultado[0][2]))
        print('Cantidad de Autores:'+ str(resultado[0][3]))
        print("Tiempo [ms]: ", f"{resultado[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[2]:.3f}")
    elif int(inputs[0]) == 4:
        print("\nBuscando musica para festejar: ")
        dance_inf =float(input("Ingrese el limite inferior de Danceability: "))
        dance_sup =float(input("Ingrese el limite superior de Danceability: "))
        temp_inf =float(input("Ingrese el limite inferior de Energy: "))
        temp_sup =float(input("Ingrese el limite superior de Energy: "))
        answer=controller.musica_festejar(catalog,dance_inf,dance_sup,temp_inf,temp_sup)
        print('La instrumentalidad está entre: ' +str(dance_inf)+' y '+str(dance_sup))
        print('El tempo está entre: ' +str(temp_inf)+' y '+str(temp_sup))
        print_fiesta(answer[0])
        
        
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
        

    elif int(inputs[0]) == 5:
        print("\nBuscando musica para estudiar: ")
        inst_inf =float(input("Ingrese el limite inferior de Instrumentalness: "))
        inst_sup =float(input("Ingrese el limite superior de Instrumentalness: "))
        BPM_inf =float(input("Ingrese el limite inferior de BPM: "))
        BPM_sup =float(input("Ingrese el limite superior de BPM: "))
        answer=controller.musica_estudiar(catalog,inst_inf,inst_sup,BPM_inf,BPM_sup)
        print('La instrumentalidad está entre: ' +str(inst_inf)+' y '+str(inst_sup))
        print('El tempo está entre: ' +str(BPM_inf)+' y '+str(BPM_sup))
        print_estudiar(answer[0])
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
    elif int(inputs[0]) == 6:
        print("\nCreando nuevo genero: ")
        genero = input("Ingrese el nombre de su nuevo genero: ").lower()
        rango_inf =float(input("Ingrese el limite inferior de BPM: "))
        rango_sup =float(input("Ingrese el limite superior de BPM: "))
        answer=controller.nuevo_genero(catalog,genero,rango_inf,rango_sup)
        print("Se creó su nuevo genero")
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    elif int(inputs[0]) == 7:
        print("\nBuscando por genero: ")
        generos = input("Ingrese los generos separados por ,: ").lower()
        resultado=controller.total_por_generos(catalog,generos)
        print("Total de reproducciónes:" +str(resultado[0][0]))
        print_generos(resultado[0])
        print("Tiempo [ms]: ", f"{resultado[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[2]:.3f}")
    elif int(inputs[0]) == 8:
        print("\nBuscando por hora: ")
        tmin = input("Ingrese el tiempo inicial: ")
        tmax=  input("Ingrese el tiempo final: ")
        resultado=controller.analisis_por_hora(catalog,tmin,tmax)
        print_horas(resultado[0],tmin,tmax)
        print("Tiempo [ms]: ", f"{resultado[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{resultado[2]:.3f}")
    else:
        sys.exit(0)
sys.exit(0)