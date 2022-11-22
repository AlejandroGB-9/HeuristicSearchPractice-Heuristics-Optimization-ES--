#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Visualización del problema, se invierte el autobús para que se desarrolle mejor el problema

#    *----*----*----*----*----*----*----*----*                     *----*----*----*----*
#    |    |    |    |    |    |    |    |    |                     |    |    |    |    |
#    *----*----*----*----*----*----*----*----*                     *----*----*----*----*
#    |    |    |    |    |    |    |    |    |                     |    |    |    |    |
#    *----*----*----*----*----*----*----*----*       --->          *----*----*----*----*
#    |    |    |    |    |    |    |    |    |                     |    |    |    |    |
#    *----*----*----*----*----*----*----*----*                     *----*----*----*----* 
#    |    |    |    |    |    |    |    |    |                     |    |    |    |    |
#    *----*----*----*----*----*----*----*----*                     *----*----*----*----* 
#                                                                  |    |    |    |    |
#                                                                  *----*----*----*----*
#                                                                  |    |    |    |    |
#                                                                  *----*----*----*----*
#                                                                  |    |    |    |    |
#                                                                  *----*----*----*----*
#                                                                  |    |    |    |    |
#                                                                  *----*----*----*----*  

#------------------------------------------------------------

from constraint import *
import csv

#Creación del problema y lectura del fichero de entrada.

problem = constraint.Problem()

data = input("Introduce el nombre del fichero de datos: ")
data.replace(".txt", ".csv")

file = open(data, "r")
alumnos_bus = list(csv.reader(file, delimiter=","))
file.close()

#------------------------------------------------------------

#Los distintos tipos de alumnos separados en listas.
alumnos_comunes_ciclo1 = []
alumnos_comunes_ciclo2 = []
alumnos_mov_reducidos_ciclo1 = []
alumnos_mov_reducidos_ciclo2 = []
alumnos_hermanos = []

#------------------------------------------------------------

#Dominios para las categorias de alumnos según los atributos recibidos.

dominio_ciclo1 = [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
dominio_ciclo2 = [(5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(7,3)]
dominio_mov_red_ciclo1 = [(0,0),(0,1),(0,2),(0,3),(3,0),(3,1),(3,2),(3,3)]
dominio_mov_red_ciclo2 = [(4,0),(4,1),(4,2),(4,3)]
dominio_no_mov_red_ciclo1 = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
dominio_no_mov_red_ciclo2 = [(4,0),(4,1),(4,2),(4,3),(5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(7,3)]
dominio_hermanos_distinto_curso = [(1,1),(1,2),(2,1),(2,2)]

#------------------------------------------------------------

#Funciones para distintos casos de alumnos.

def no_mov_redc_ciclo1():
    #Si no hay alumnos con movilidad reducida en ciclo 1, se asigna el dominio de los alumnos sin movilidad reducida para ciclo 1.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i][0], dominio_no_mov_red_ciclo1)
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i][0], dominio_ciclo2)  
    for i in range(0, len(alumnos_mov_reducidos_ciclo2)):
        problem.addVariable(alumnos_mov_reducidos_ciclo2[i], dominio_mov_red_ciclo2)

def no_mov_redc_ciclo2():
    #Si no hay alumnos con movilidad reducida en ciclo 2, se asigna el dominio de los alumnos sin movilidad reducida para ciclo 2.
    
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i][0], dominio_no_mov_red_ciclo2)
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i][0], dominio_ciclo1)  
    for i in range(0, len(alumnos_mov_reducidos_ciclo1)):
        problem.addVariable(alumnos_mov_reducidos_ciclo1[i], dominio_mov_red_ciclo1)
       
def no_mov_redc():
    #Si no hay alumnos con movilidad reducida, se asigna el dominio de los alumnos sin movilidad reducida.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i][0], dominio_no_mov_red_ciclo1)
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i][0], dominio_no_mov_red_ciclo2)

def asign_domain_alumnos():
    #En caso de alumnos con mov.reducida.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i][0], dominio_ciclo1)
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i][0], dominio_ciclo2)  
    for i in range(0, len(alumnos_mov_reducidos_ciclo1)):
        problem.addVariable(alumnos_mov_reducidos_ciclo1[i][0], dominio_mov_red_ciclo1) 
    for i in range(0, len(alumnos_mov_reducidos_ciclo2)):
        problem.addVariable(alumnos_mov_reducidos_ciclo2[i][0], dominio_mov_red_ciclo2)

#------------------------------------------------------------

#Alumnos a sus listas correspondientes
for i in range(0, len(alumnos_bus)):
    if int(alumnos_bus[i][0]) != 0:
        hermanos = (alumnos_bus[i][0], alumnos_bus[i][4])
        if (hermanos[0][0],hermanos[0][1]) or (hermanos[0][1],hermanos[0][0]) not in alumnos_hermanos:
            alumnos_hermanos.append(hermanos)

#TODO: hacer que los alumnos de distintos ciclos que sean hermanos se le ponga al mayor el dominio de los pasillos del ciclo 1.

    if alumnos_bus[i][1] == "1":
        if alumnos_bus[i][2] == "R":
            alumnos_mov_reducidos_ciclo1.append(alumnos_bus[i][0])
        else:
            alumnos_comunes_ciclo1.append(alumnos_bus[i])
    elif alumnos_bus[i][1] == "2":
        if alumnos_bus[i][2] == "R":
            alumnos_mov_reducidos_ciclo2.append(alumnos_bus[i][0])
        else:
            alumnos_comunes_ciclo2.append(alumnos_bus[i])

#------------------------------------------------------------

#Se añaden las variables al problema según el caso del problema.
if (len(alumnos_mov_reducidos_ciclo1) == 0):
    no_mov_redc_ciclo1()
    
elif (len(alumnos_mov_reducidos_ciclo2) == 0):
    no_mov_redc_ciclo2()
    
elif (len(alumnos_mov_reducidos_ciclo1) == 0) and (len(alumnos_mov_reducidos_ciclo2) == 0):
    no_mov_redc()
    
else:
    asign_domain_alumnos()
       
        
    