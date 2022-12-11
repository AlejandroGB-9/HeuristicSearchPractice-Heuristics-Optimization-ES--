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
#Importamos las librerías necesarias para el funcionamiento del programa.

import constraint
from constraint import *
import csv
import random
import sys
import os.path
import pathlib

#Creación del problema y lectura del fichero de entrada.

problem = constraint.Problem()

#Se guarda el archivo de entrada introducido por terminal en una variable.

data = sys.argv[1]    
data.replace(".txt", ".csv")

#Leemos el archivo de entrada y se guardan los datos leidos en una lista.

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

#En el caso de no haber alumnos con movilidad reducida, se asigna aquellos asientos de movilidad reducida a los alumnos comunes.

dominio_no_mov_red_ciclo1 = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
dominio_no_mov_red_ciclo2 = [(4,0),(4,1),(4,2),(4,3),(5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(7,3)]

#En caso de que dos hermanos tengan distintos cursos, se asigna el dominio del menor que corresponde al ciclo 1.

dominio_hermanos_distinto_curso = [(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
dominio_hermanos_distinto_curso_no_mov_red_c1 = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]

#------------------------------------------------------------

#Counters para los hermanos de mov.reducida de los ciclos 1 y 2.

count_herm_movred_c1 = 0
count_herm_movred_c2 = 0

#------------------------------------------------------------

#Función para buscar un hermano

def buscar_hermano(a):
    #Función para buscar un hermano.
    for i in range (len(alumnos_bus)):
        
        if alumnos_bus[i][0] == a:

            return alumnos_bus[i]

#------------------------------------------------------------

#Funciones para distintos casos de alumnos.

def no_mov_redc_ciclo1():
    #Si no hay alumnos con movilidad reducida en ciclo 1, se asigna el dominio de los alumnos sin movilidad reducida para los alumnos comunes del ciclo 1.
    
    #Dominio para los alumnos comunes
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo1[i]), dominio_no_mov_red_ciclo1)
        
    for i in range(0, len(alumnos_comunes_ciclo2)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo2[i]), dominio_ciclo2)  
        
    for i in range(0, len(alumnos_mov_reducidos_ciclo2)):
        
        problem.addVariable(tuple(alumnos_mov_reducidos_ciclo2[i]), dominio_mov_red_ciclo2)
    
    #Dominio para los hermanos
    
    while i < len(alumnos_hermanos):
        
        #Caso para solo un hermano con movilidad reducida.
        #El que no es de movilidad reducida se le asigna el dominio del ciclo del hermano con movilidad reducida para que le pueda ayudar estando próximo a él.
        
        #Hermanos con el mismo ciclo.
        
        if (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_no_mov_red_ciclo1)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_no_mov_red_ciclo1)
            
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            
            #Caso para los dos hermanos con movilidad reducida.
            
            if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] != "R":
            
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo2)
                
            elif alumnos_hermanos[i+1][2] == "R" and alumnos_hermanos[i][2] != "R":
            
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo2)
                
            elif alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] == "R":
            
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo2)
                
            else:
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo2)
         
        #Hermanos con distinto ciclo.
        #Se asigna el dominio del menor que corresponde al ciclo 1 a ambos.
            
        elif alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            
            problem.addVariable(tuple(alumnos_hermanos[i][0]), dominio_hermanos_distinto_curso_no_mov_red_c1)
            problem.addVariable(tuple(alumnos_hermanos[i+1][0]), dominio_hermanos_distinto_curso_no_mov_red_c1)
        
        i+=2  
      
        

def no_mov_redc_ciclo2():
    #Si no hay alumnos con movilidad reducida en ciclo 2, se asigna el dominio de los alumnos sin movilidad reducida para ciclo 2.
    
    #Dominio para los alumnos comunes
    
    for i in range(0, len(alumnos_comunes_ciclo2)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo2[i]), dominio_no_mov_red_ciclo2)
        
    for i in range(0, len(alumnos_comunes_ciclo1)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo1[i]), dominio_ciclo1)  
        
    for i in range(0, len(alumnos_mov_reducidos_ciclo1)):
        
        problem.addVariable(tuple(alumnos_mov_reducidos_ciclo1[i]), dominio_mov_red_ciclo1)
        
    #Dominio para los hermanos    
        
    #Caso para solo un hermano con movilidad reducida.
        #El que no es de movilidad reducida se le asigna el dominio del ciclo del hermano con movilidad reducida para que le pueda ayudar estando próximo a él.
        
        #Hermanos con el mismo ciclo.
        
        if (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_no_mov_red_ciclo2)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_no_mov_red_ciclo2)
            
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            
            #Caso para los dos hermanos con movilidad reducida.
            
            if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] != "R":
            
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo1)
                
            elif alumnos_hermanos[i+1][2] == "R" and alumnos_hermanos[i][2] != "R":
            
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo1)
                
            elif alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] == "R":
            
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo1)
                
            else:
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo1)
         
        #Hermanos con distinto ciclo.
        #Se asigna el dominio del menor que corresponde al ciclo 1 a ambos.
            
        elif alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            
            problem.addVariable(tuple(alumnos_hermanos[i][0]), dominio_hermanos_distinto_curso)
            problem.addVariable(tuple(alumnos_hermanos[i+1][0]), dominio_hermanos_distinto_curso)
        
        i+=2  
       
def no_mov_redc():
    #Si no hay alumnos con movilidad reducida, se asigna el dominio de los alumnos sin movilidad reducida.
    
    #Dominio para los alumnos comunes
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo1[i]), dominio_no_mov_red_ciclo1)
        
    for i in range(0, len(alumnos_comunes_ciclo2)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo2[i]), dominio_no_mov_red_ciclo2)
        
    #Dominio para los hermanos.
        
    while i < len(alumnos_hermanos):
        
        #Hermanos con distinto ciclo.
        #Se asigna el dominio del menor que corresponde al ciclo 1 a ambos.
        
        if alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_hermanos_distinto_curso_no_mov_red_c1)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_hermanos_distinto_curso_no_mov_red_c1)
            
        #Hermanos con mismo ciclo.
            
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_no_mov_red_ciclo1)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_no_mov_red_ciclo1)
            
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_no_mov_red_ciclo2)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_no_mov_red_ciclo2)
        
        i+=2  

def asign_domain_alumnos():
    #En caso de alumnos con mov.reducida en ambos ciclos.
    
    #Dominio para los alumnos comunes.
    
    for i in range(0, len(alumnos_comunes_ciclo1)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo1[i]), dominio_ciclo1)
        
    for i in range(0, len(alumnos_comunes_ciclo2)):
        
        problem.addVariable(tuple(alumnos_comunes_ciclo2[i]), dominio_ciclo2)
        
    #Dominio para los alumnos con movilidad reducida.
          
    for i in range(0, len(alumnos_mov_reducidos_ciclo1)):
        
        problem.addVariable(tuple(alumnos_mov_reducidos_ciclo1[i]), dominio_mov_red_ciclo1) 
        
    for i in range(0, len(alumnos_mov_reducidos_ciclo2)):
        
        problem.addVariable(tuple(alumnos_mov_reducidos_ciclo2[i]), dominio_mov_red_ciclo2)
        
    #Dominio para los hermanos.
        
    while i < len(alumnos_hermanos):
        
        #Caso para solo un hermano con movilidad reducida.
        #El que no es de movilidad reducida se le asigna el dominio del ciclo del hermano con movilidad reducida para que le pueda ayudar estando próximo a él.
        
        if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] != "R":
            
            if alumnos_hermanos[i][1] == "1":
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo1)
                
            elif alumnos_hermanos[i][1] == "2":
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo2)
                
        elif alumnos_hermanos[i+1][2] == "R" and alumnos_hermanos[i][2] != "R":
            
            if alumnos_hermanos[i+1][1] == "1":
                
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo1)
                
            elif alumnos_hermanos[i+1][1] == "2":
                
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo2)
                
        #Caso para los dos hermanos con movilidad reducida.
                
        elif alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i+1][2] == "R":
            
            if alumnos_hermanos[i][1] == "1" and alumnos_hermanos[i+1][1] == "1":
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo1)
                
            elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "2":
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo2)
                
            elif alumnos_hermanos[i][1] == "1" and alumnos_hermanos[i+1][1] == "2":
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo1)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo2)
                
            elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i+1][1] == "1":
                
                problem.addVariable(tuple(alumnos_hermanos[i]), dominio_mov_red_ciclo2)
                problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_mov_red_ciclo1)
                
        #Hermanos con distinto ciclo.
        #Se asigna el dominio del menor que corresponde al ciclo 1 a ambos.
                
        elif alumnos_hermanos[i][1] != alumnos_hermanos[i+1][1]:
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_hermanos_distinto_curso)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_hermanos_distinto_curso)
            
        #Hermanos con mismo ciclo.
            
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "1":
            
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo1)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo1)
            
        elif (alumnos_hermanos[i][1] and alumnos_hermanos[i+1][1]) == "2":
            problem.addVariable(tuple(alumnos_hermanos[i]), dominio_ciclo2)
            problem.addVariable(tuple(alumnos_hermanos[i+1]), dominio_ciclo2)
        
        i+=2  

#------------------------------------------------------------

#Se registran los alumnos en sus listas correspondientes.
for i in range(0, len(alumnos_bus)):
    
    #En el caso de que el alumno tenga un hermano. Se busca el hermanos y se registran.
    #Los hermanos se registran "sueltos" pero al añadirse a la par no daría problemas al hacer un i y i+1 siempre que se haga un i+=2 en bucles.
    
    if int(alumnos_bus[i][4]) != 0:
        
        hermano = buscar_hermano(alumnos_bus[i][4])
        
        if (alumnos_bus[i] and hermano) not in alumnos_hermanos:
            
            alumnos_hermanos.append(alumnos_bus[i])
            alumnos_hermanos.append(hermano)
    
    #En el caso de que el alumno no tenga hermanos.
    
    else:
        
        #Se comprueban los ciclos y si son de movilidad reducida.
        
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

#Se compruba si existen alumnos de movilidad reducida.

#En el caso de que hayan hermanos se comprueba si hay alumnos de movilidad reducida.

if len(alumnos_hermanos) != 0:
    
    for i in range(len(alumnos_hermanos)):
        
        if alumnos_hermanos[i][1] == "1" and alumnos_hermanos[i][2] == "R":
                
            count_herm_movred_c1 += 1
                
        elif alumnos_hermanos[i][1] == "2" and alumnos_hermanos[i][2] == "R":
                
                count_herm_movred_c2 += 1     

#Caso en el que no hay alumnos de movilidad reducida en el ciclo 1.

if (len(alumnos_mov_reducidos_ciclo1) == 0) and count_herm_movred_c1 == 0:
    
    no_mov_redc_ciclo1()
 
#Caso en el que no hay alumnos de movilidad reducida en el ciclo 2. 
    
elif (len(alumnos_mov_reducidos_ciclo2) == 0) and count_herm_movred_c2 == 0:
    
    no_mov_redc_ciclo2()
    
#Caso en el que no hay alumnos de movilidad reducida.    
    
elif (len(alumnos_mov_reducidos_ciclo1) == 0) and (len(alumnos_mov_reducidos_ciclo2) == 0) and count_herm_movred_c2 == 0 and count_herm_movred_c1 == 0:
    
    no_mov_redc()

#Caso en el que existen alumnos de movilidad reducida en los dos ciclos.
    
else:
    
    asign_domain_alumnos()

#------------------------------------------------------------

#Funciones para restricciones.

def conflictivos(a,b):
    
    #Un alumno conflictivo no puede tener otros alumnos alrededor.
    
    #Se comprueba si los alumnos están en la misma fila, esto es la horizontal de la matriz.
    #Si la diferencia entre ambos alumnos en mayor a 1 entre los asientos de al lado, se devuelve True.
    
    if a[0] == b[0] and abs(a[1] - b[1]) > 1:
        
        return True
    
    #Se comprueba el mismo caso de la horizontal para la horizontal de arriba y de abajo. Es decir, la fila de de arriba y la de abajo al alumno conflictivo.
    
    if (a[0] + 1) == b[0] and abs(a[1] - b[1]) > 1:
        
        return True

    if (a[0] - 1) == b[0] and abs(a[1] - b[1]) > 1:
        
        return True

def mov_reducida(a,b):
    
    #Un alumno con movilidad reducida no puede tener otros alumnos en el asiento de al lado.
    #Se comprueba que en las secciones de movilidad reducida si un asiento de una fila especifica está ocupado, el asiento de al lado no puede estar ocupado.
    
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
    #Esto es, tengan mismo ciclo o no según, el dominio de los hermanos será el mismo y han de estar al lado.
    #La diferencia entre uno y otro en asientos de la horizontal o fila debe ser 1.
    
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and ((a[1] != 1 and b[1] != 2) or (a[1] != 2 and b[1] != 1)):
        
        return True
    
def hermanos_conflictivos(a,b,c):
    
    #Los dos hermanos conflictivos no pueden tener nadie alrededor.
    #Se realizan las misma comprobaciones que en la función conflictivos.
    #Las comprobaciones se realizan simultaneamente para los dos hermanos conflictivos ante otro alumno.
    
    if (a[0] == b[0]) and (abs(a[1] - b[1]) == 1) and ((a[1] != 1 and b[1] != 2) or (a[1] != 2 and b[1] != 1)):
        
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

def hermanos_distinto_ciclo(a,b):
    
    #Dos alumnos que sean hermanos deben estar sentados uno al lado del otro. En este caso, 'a' es el hermano menor y 'b' el mayor.
    #Al ser de distintos ciclos, el hermano mayor debe tener el dominio de los pasillos del ciclo 1.
    
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and ((a[1] != 1 and b[1] != 2) or (a[1] != 2 and b[1] != 1)) and (b[1] == 1 or b[1] == 2):
        
        return True
#------------------------------------------------------------

#Se añaden las restricciones al problema.

#Movilidad reducida.

#Se añaden las restricciones de movilidad reducida para los alumnos que la tengan según su ciclo.

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
               
#Hermanos con movilidad reducidoa ante los otros alumnos de movilidad reducida.

while i < len(alumnos_hermanos):
    
    if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i][1] == "1":
        
        for j in range(len(alumnos_mov_reducidos_ciclo1)):
            
            problem.addConstraint(mov_reducida, (alumnos_hermanos[i], alumnos_mov_reducidos_ciclo1[j]))
            
    if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i][1] == "2":  
         
        for y in range(len(alumnos_mov_reducidos_ciclo2)):
            
            problem.addConstraint(mov_reducida, (alumnos_hermanos[i], alumnos_mov_reducidos_ciclo2[y]))  
             
    i+=1
    
#Hermanos con movilidad reducida ante los otros alumnos de movilidad reducida en hermanos.

while i < len(alumnos_hermanos):
    
    for j in range(len(alumnos_hermanos)):
        
        if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i][1] == "1" and alumnos_hermanos[j][2] == "R" and alumnos_hermanos[j][1] == "1" and i != j:
        
           problem.addConstraint(mov_reducida, (alumnos_hermanos[i], alumnos_hermanos[j]))
            
        if alumnos_hermanos[i][2] == "R" and alumnos_hermanos[i][1] == "2" and alumnos_hermanos[j][2] == "R" and alumnos_hermanos[j][1] == "2" and i != j:
            
            problem.addConstraint(mov_reducida, (alumnos_hermanos[i], alumnos_hermanos[j]))
             
    i+=1   
    
#Hermanos conflictivos.

while i < len(alumnos_hermanos):
    
    #Ambos hermanos son conflictivos, se comprueba con todos los alumnos del autobus.
    
    if alumnos_hermanos[i][3] == alumnos_hermanos[i+1][3] and alumnos_hermanos[i][3] == "C":
        
        for j in range(len(alumnos_bus)):
            
            if alumnos_bus[j] != alumnos_hermanos[i] and alumnos_bus[j] != alumnos_hermanos[i+1]:
                
                problem.addConstraint(hermanos_conflictivos, (alumnos_hermanos[i], alumnos_hermanos[i+1], alumnos_bus[j]))
                
    #Solo uno de los hermanos es conflictivo, se comprueba con todos los alumnos del autobus.
    
    if alumnos_hermanos[i][3] != alumnos_hermanos[i+1][3] and (alumnos_hermanos[i][3] or alumnos_hermanos[i+1][3]) == "C":
        
        for j in range(len(alumnos_bus)):
            
            if alumnos_hermanos[i][3] == "C":
                
                if alumnos_bus[j] != alumnos_hermanos[i]:
                    
                    problem.addConstraint(conflictivos, (alumnos_hermanos[i], alumnos_bus[j])) 
                    
            elif alumnos_hermanos[i+1][3] == "C":
                
                if alumnos_bus[j] != alumnos_hermanos[i+1]:
                    
                    problem.addConstraint(conflictivos, (alumnos_hermanos[i+1], alumnos_bus[j]))  
                    
    i += 2

#Hermanos.

while i < len(alumnos_hermanos):
    
    if alumnos_hermanos[i][1] == alumnos_hermanos[i+1][1]:
        
        problem.addConstraint(hermanos_ciclos, (alumnos_hermanos[i], alumnos_hermanos[i+1]))
        
    if alumnos_hermanos[i][1] < alumnos_hermanos[i+1][1]:
        
        problem.addConstraint(hermanos_distinto_ciclo, (alumnos_hermanos[i], alumnos_hermanos[i+1]))
        
    if alumnos_hermanos[i][1] > alumnos_hermanos[i+1][1]:
        
        problem.addConstraint(hermanos_distinto_ciclo, (alumnos_hermanos[i+1], alumnos_hermanos[i]))
        
    i += 2

#Conflictivos.

for i in range(len(alumnos_bus)):
    
    #Se comprueba si el alumno es conflictivo. Además no debe estar en alumnos_hermanos ya que se ha comprobado anteriormente.
    
    if alumnos_bus[i][3] == "C" and alumnos_bus[i] not in alumnos_hermanos:
        
        for j in range(len(alumnos_bus)):
            
            if i != j and alumnos_bus[j] not in alumnos_hermanos:
                
                problem.addConstraint(conflictivos, (alumnos_bus[i], alumnos_bus[j]))

#Todos los alumnos deben tener asientos diferentes.

problem.addConstraint(AllDifferentConstraint())

#------------------------------------------------------------

#Conseguir las soluciones.

soluciones = problem.getSolutions()

#Solución aleatoria.

solucion = random.choice(soluciones)

#------------------------------------------------------------

#Imprimir las soluciones en un archivo de texto con extensión '.output', inversión de la matriz.

n_soluciones = len(soluciones)
text_solution = {}

#Se crea un diccionario con los alumnos y su posición en el autobus.

for i in range(len(alumnos_bus)):
    
    alumno = str(alumnos_bus[i][0] + alumnos_bus[i][3] + alumnos_bus[i][2])
    for key, value in solucion.items(): 
        
        alumnos_sol = str(key[0] + key[3] + key[2])
        if alumno == alumnos_sol:
            
            position = value[0]*4 + value[1] + 1
            text_solution[alumno] = position
   
#Se crea el archivo de salida dada los solución escogida.   
            
output_file = ""
for i in range(len(data)):
    if data[i] == ".":
        break
    output_file += data[i]
output_file += ".output"
path = pathlib.Path(__file__).parent.resolve()
output_file = os.path.join(path, output_file)
file_output = open(output_file, "w")
file_output.write("Número de soluciones: " + str(n_soluciones) + "\n")
file_output.write(str(text_solution))
file_output.close()


#------------------------------------------------------------        
        