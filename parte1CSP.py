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

#counters para los hermanos de mov.reducida de los ciclos 1 y 2.

count_herm_movred_c1 = 0
count_herm_movred_c2 = 0

#------------------------------------------------------------

#Función para buscar un hermano

def buscar_hermano(a):
    #Función para buscar un hermano.
    for i in range (0,len(alumnos_hermanos)):
        if a == i[0]:
            return i

#------------------------------------------------------------

#Funciones para distintos casos de alumnos.

def no_mov_redc_ciclo1():
    #Si no hay alumnos con movilidad reducida en ciclo 1, se asigna el dominio de los alumnos sin movilidad reducida para ciclo 1.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i], dominio_no_mov_red_ciclo1)
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i], dominio_ciclo2)  
    for i in range(0, len(alumnos_mov_reducidos_ciclo2)):
        problem.addVariable(alumnos_mov_reducidos_ciclo2[i], dominio_mov_red_ciclo2)
    while i < len(alumnos_hermanos):
        if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] != "R":
            if alumnos_hermanos[i][1] == "2":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        elif alumnos_hermanos[i+1][2] == "R" and alumnos_hermanos[i][2] != "R":
            if alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
            elif alumnos_hermanos[i+1][1] == "2":
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i], dominio_ciclo2)
        elif alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] == "R":
            if alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "2":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo2)
            elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
        elif alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            problem.addVariable(alumnos_hermanos[i][0], dominio_hermanos_distinto_curso)
            problem.addVariable(alumnos_hermanos[i+1][0], dominio_hermanos_distinto_curso)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo1)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo2)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        
        i+=2  
      
        

def no_mov_redc_ciclo2():
    #Si no hay alumnos con movilidad reducida en ciclo 2, se asigna el dominio de los alumnos sin movilidad reducida para ciclo 2.
    
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i], dominio_no_mov_red_ciclo2)
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i], dominio_ciclo1)  
    for i in range(0, len(alumnos_mov_reducidos_ciclo1)):
        problem.addVariable(alumnos_mov_reducidos_ciclo1[i], dominio_mov_red_ciclo1)
    while i < len(alumnos_hermanos):
        if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] != "R":
            if alumnos_hermanos[i][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo1)
            elif alumnos_hermanos[i][1] == "2":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        elif alumnos_hermanos[i+1][2] == "R" and alumnos_hermanos[i][2] != "R":
            if alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
        elif alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] == "R":
            if alumnos_hermanos[i][1] == "1" and alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
            elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
        elif alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            problem.addVariable(alumnos_hermanos[i][0], dominio_hermanos_distinto_curso)
            problem.addVariable(alumnos_hermanos[i+1][0], dominio_hermanos_distinto_curso)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo1)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo2)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        
        i+=2  
       
def no_mov_redc():
    #Si no hay alumnos con movilidad reducida, se asigna el dominio de los alumnos sin movilidad reducida.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i], dominio_no_mov_red_ciclo1)
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i], dominio_no_mov_red_ciclo2)
    while i < len(alumnos_hermanos):
        if alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            problem.addVariable(alumnos_hermanos[i][0], dominio_hermanos_distinto_curso)
            problem.addVariable(alumnos_hermanos[i+1][0], dominio_hermanos_distinto_curso)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo1)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo2)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        
        i+=2  

def asign_domain_alumnos():
    #En caso de alumnos con mov.reducida.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        problem.addVariable(alumnos_comunes_ciclo1[i], dominio_ciclo1)
    for i in range(0, len(alumnos_comunes_ciclo2)):
        problem.addVariable(alumnos_comunes_ciclo2[i], dominio_ciclo2)  
    for i in range(0, len(alumnos_mov_reducidos_ciclo1)):
        problem.addVariable(alumnos_mov_reducidos_ciclo1[i], dominio_mov_red_ciclo1) 
    for i in range(0, len(alumnos_mov_reducidos_ciclo2)):
        problem.addVariable(alumnos_mov_reducidos_ciclo2[i], dominio_mov_red_ciclo2)
    while i < len(alumnos_hermanos):
        if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] != "R":
            if alumnos_hermanos[i][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo1)
            elif alumnos_hermanos[i][1] == "2":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        elif alumnos_hermanos[i+1][2] == "R" and alumnos_hermanos[i][2] != "R":
            if alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
            elif alumnos_hermanos[i+1][1] == "2":
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i], dominio_ciclo2)
        elif alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] == "R":
            if alumnos_hermanos[i][1] == "1" and alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
            elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "2":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo2)
            elif alumnos_hermanos[i][1] == "1" and alumnos_hermanos[i+1][1] == "2":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo1)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo2)
            elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "1":
                problem.addVariable(alumnos_hermanos[i], dominio_mov_red_ciclo2)
                problem.addVariable(alumnos_hermanos[i+1], dominio_mov_red_ciclo1)
        elif alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            problem.addVariable(alumnos_hermanos[i][0], dominio_hermanos_distinto_curso)
            problem.addVariable(alumnos_hermanos[i+1][0], dominio_hermanos_distinto_curso)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo1)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo1)
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            problem.addVariable(alumnos_hermanos[i], dominio_ciclo2)
            problem.addVariable(alumnos_hermanos[i+1], dominio_ciclo2)
        
        i+=2  

#------------------------------------------------------------

#Alumnos a sus listas correspondientes
for i in range(0, len(alumnos_bus)):
    if int(alumnos_bus[i][4]) != 0:
        hermano = buscar_hermano(alumnos_bus[i][4])
        if alumnos_bus[i] not in alumnos_hermanos:
            alumnos_hermanos.append(alumnos_bus[i])
            alumnos_hermanos.append(hermano)
    
    else:
        
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
if len(alumnos_hermanos) != 0:
    for i in range(0,len(alumnos_hermanos)):
        if alumnos_hermanos[i][1] == "1":
            if alumnos_hermanos[i][2] == "R":
                count_herm_movred_c1 += 1
        elif alumnos_hermanos[i][1] == "2":
            if alumnos_hermanos[i][2] == "R":
                count_herm_movred_c2 += 1     

if (len(alumnos_mov_reducidos_ciclo1) == 0) and count_herm_movred_c1 == 0:
    no_mov_redc_ciclo1()
    
elif (len(alumnos_mov_reducidos_ciclo2) == 0) and count_herm_movred_c2 == 0:
    no_mov_redc_ciclo2()
    
elif (len(alumnos_mov_reducidos_ciclo1) == 0) and (len(alumnos_mov_reducidos_ciclo2) == 0) and count_herm_movred_c2 == 0 and count_herm_movred_c1 == 0:
    no_mov_redc()
    
else:
    asign_domain_alumnos()

#------------------------------------------------------------

#Funciones para restricciones.

def conflictivos(a,b):
    #Un alumno conflictivo no puede tener otros alumnos alrededor.
    if a[0] == b[0] and abs(a[1] - b[1]) > 1:
        return True
    
    if a[1] == b[1] and abs(a[0] - b[0]) > 1:
        return True
    
    if (a[0] + 1) == b[0] and abs(a[1] - b[1]) > 1:
        return True

    if (a[0] - 1) == b[0] and abs(a[1] - b[1]) > 1:
        return True

def mov_reducida(a,b):
    #Un alumno con movilidad reducida no puede tener otros alumnos en el asiento de al lado.
    if a[1] == 0 and b[1] != 1 and a[0] == b[0]:
        return True
    
    if a[1] == 1 and b[1] != 0 and a[0] == b[0]:
        return True
    
    if a[1] == 2 and b[1] != 3 and a[0] == b[0]:
        return True
    
    if a[1] == 3 and b[1] != 2 and a[0] == b[0]:
        return True

def hermanos_ciclos(a,b):  
    #Dos alumnos que sean hermanos deben estar sentados uno al lado del otro.
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and ((a[1] != 1 and b[1] != 2) or (a[1] != 2 and b[1] != 1)):
        return True
    
def hermanos_conflictivos(a,b,c):
    #Los dos hermanos conflictivos no pueden tener nadie alrededor.
    if (a[0] == b[0]) and (abs(a[1] - b[1]) == 1) and (a[0]>b[0]):
        
        if a[0] == c[0] and (a[1] - c[1]) > 1:
            return True
        
        if b[0] == c[0] and (c[1] - b[1]) > 1:
            return True
        
        if (a[0] + 1) == c[0] and (a[1] - c[1]) > 1:
            return True
        
        if(b[0] + 1) == c[0] and (c[1] - b[1]) > 1:
            return True
        
        if (a[0] - 1) == c[0] and (a[1] - c[1]) > 1:
            return True
        
        if (b[0] - 1) == c[0] and (c[1] - b[1]) > 1:
            return True
        
    if (a[0] == b[0]) and (abs(a[1] - b[1]) == 1) and (b[0]>a[0]):
        
        if b[0] == c[0] and (b[1] - c[1]) > 1:
            return True
        
        if a[0] == c[0] and (c[1] - a[1]) > 1:
            return True
        
        if (b[0] + 1) == c[0] and (b[1] - c[1]) > 1:
            return True
        
        if(a[0] + 1) == c[0] and (c[1] - a[1]) > 1:
            return True
        
        if (b[0] - 1) == c[0] and (b[1] - c[1]) > 1:
            return True
        
        if (a[0] - 1) == c[0] and (c[1] - a[1]) > 1:
            return True

def hermanos_distinto_ciclo(a,b):
    #Dos alumnos que sean hermanos deben estar sentados uno al lado del otro. En este caso, 'a' es el hermano menor y 'b' el mayor.
    #Al ser de distintos ciclos, el hermano mayor debe tener el dominio de los pasillos del ciclo 1.
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and ((a[1] != 1 and b[1] != 2) or (a[1] != 2 and b[1] != 1)) and (b[1] == 1 or b[1] == 2):
        return True
#------------------------------------------------------------

#Se añaden las restricciones al problema.

#Movilidad reducida.
if len(alumnos_mov_reducidos_ciclo1) != 0:
    for i in range(len(alumnos_mov_reducidos_ciclo1)):
        for j in range(len(alumnos_mov_reducidos_ciclo1)):
            if i != j:
                problem.addConstraint(mov_reducida, (alumnos_mov_reducidos_ciclo1[i], alumnos_mov_reducidos_ciclo1[j]))

if len(alumnos_mov_reducidos_ciclo2) != 0:
    for i in range(len(alumnos_mov_reducidos_ciclo2)):
        for j in range(len(alumnos_mov_reducidos_ciclo2)):
            if i != j:
                problem.addConstraint(mov_reducida, (alumnos_mov_reducidos_ciclo2[i], alumnos_mov_reducidos_ciclo2[j]))
               
#Hermanos reducido.

while i < len(alumnos_hermanos):
    if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i][1] == "1":
        for j in range(len(alumnos_mov_reducidos_ciclo1)):
            problem.addConstraint(mov_reducida, (alumnos_hermanos[i], alumnos_mov_reducidos_ciclo1[j]))
    if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i][1] == "2":   
        for y in range(len(alumnos_mov_reducidos_ciclo2)):
            problem.addConstraint(mov_reducida, (alumnos_hermanos[i], alumnos_mov_reducidos_ciclo2[y]))   
    i+=1

#Hermanos.

while i < len(alumnos_hermanos):
    if alumnos_hermanos[i][1] == alumnos_hermanos[i+1][1]:
        problem.addConstraint(hermanos_ciclos, (alumnos_hermanos[i], alumnos_hermanos[i+1]))
    if alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
        problem.addConstraint(hermanos_distinto_ciclo, (alumnos_hermanos[i], alumnos_hermanos[i+1]))
        
    i += 2
        
#Hermanos conflictivos.

while i < len(alumnos_hermanos):
    if alumnos_hermanos[i][3] == alumnos_hermanos[i+1][3] and alumnos_hermanos[i][3] == "C":
        for j in range(len(alumnos_bus)):
            if j != i and j != i+1:
                problem.addConstraint(hermanos_conflictivos, (alumnos_hermanos[i], alumnos_hermanos[i+1], alumnos_bus[j]))
    if alumnos_hermanos[i][3] != alumnos_hermanos[i+1][3] and (alumnos_hermanos[i][3] or alumnos_hermanos[i+1][3]) == "C":
        for j in range(len(alumnos_bus)):
            if alumnos_hermanos[i][3] == "C":
                if j != i:
                    problem.addConstraint(conflictivos, (alumnos_hermanos[i], alumnos_bus[j])) 
            elif alumnos_hermanos[i+1][3] == "C":
                if j != i+1:
                    problem.addConstraint(conflictivos, (alumnos_hermanos[i+1], alumnos_bus[j]))  
    i += 2

#Conflictivos.

for i in range(len(alumnos_bus)):
    if alumnos_bus[i][3] == "C":
        for j in range(len(alumnos_bus)):
            if i != j:
                problem.addConstraint(conflictivos, (alumnos_bus[i], alumnos_bus[j]))

#------------------------------------------------------------

#Conseguir las soluciones.

#------------------------------------------------------------

#Imprimir las soluciones en un archivo de texto con extensión '.output', inversión de la matriz.

#------------------------------------------------------------        
        
        
    