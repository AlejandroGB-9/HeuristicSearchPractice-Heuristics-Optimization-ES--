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

data = "hola.txt"    
data.replace(".txt", ".csv")

#Leemos el archivo de entrada y se guardan los datos leidos en una lista de tuplas.

file = open(data, "r")
alumnos_bus = [tuple(line) for line in csv.reader(file, delimiter=",")]
file.close()

#------------------------------------------------------------

#Los distintos tipos de alumnos separados en listas.
alumnos_comunes = []
alumnos_conflictivos = []
alumnos_mov_reducida = []
alumnos_mov_reducida_conflictivos = []
alumnos_hermanos = []

#------------------------------------------------------------

#Dominios para las categorias de alumnos según los atributos recibidos.

dominio_ciclo1 = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
dominio_ciclo2 = [(4,0),(4,1),(4,2),(4,3),(5,0),(5,1),(5,2),(5,3),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(7,3)]
dominio_mov_red_ciclo1 = [(0,0),(0,1),(0,2),(0,3),(3,0),(3,1),(3,2),(3,3)]
dominio_mov_red_ciclo2 = [(4,0),(4,1),(4,2),(4,3)] 
        
#------------------------------------------------------------

#Se registran los alumnos en sus listas correspondientes.
for i in alumnos_bus:
    
    #En el caso de que el alumno tenga un hermano. Se busca el hermanos y se registran.
    #Siempre se comprueba que los hermanos no estén ya registrados. Así evitamos que se dupliquen.
    
    if i[4] != "0":
        index_hermano = int(i[4]) - 1
        
        hermano = alumnos_bus[index_hermano]
        
        if i not in alumnos_hermanos and hermano not in alumnos_hermanos:
            
            alumnos_hermanos.append(i)
            alumnos_hermanos.append(hermano)
    
    #En el caso de que el alumno no tenga hermanos.
    
    elif i[4] == "0":
        
        #Se comprueban los ciclos y si son de movilidad reducida, conflictivos o ambos.
        #Según el caso, se añaden a las listas correspondientes.
        
        if i[2] == "C":
            
            if i[3] == "R":
                
                alumnos_mov_reducida_conflictivos.append(i)
                
            else:
                
                alumnos_conflictivos.append(i)
                
        elif i[3] == "R":
            
            alumnos_mov_reducida.append(i)
                
        else:
            
            alumnos_comunes.append(i)

#------------------------------------------------------------

#Se añaden las variables al problema.
    
for i in alumnos_bus:
        
        if i in alumnos_hermanos:
            
            pass
        
        else:
            
            #Se comprube a que ciclo pertenece el alumno y si es de movilidad reducida.
            
            if i[1] == "1":
                    
                if i[3] == "R":
                        
                    problem.addVariable(i, dominio_mov_red_ciclo1) 
                    
                else:
                    
                    problem.addVariable(i, dominio_ciclo1)
                    
            elif i[1] == "2":
                    
                if i[3] == "R":
                        
                    problem.addVariable(i, dominio_mov_red_ciclo2)
                    
                else:
                    
                    problem.addVariable(i, dominio_ciclo2)
     
     #Para los hermanos, nos aseguramos que la i sea impar para coger al hermano y que luego no se duplique y de problemas con el siguiente alumno en la lista.
j = 1
hermano = 0
                 
for i in alumnos_hermanos:
    
    if j % 2 != 0:
        
        hermano = i
        pass
    
    else:
        
        #Se comprueba las caracteristicas de los hermanos para añadirlas como variables al problema según sean.
        #En otras palabras, se comprueba si son de movilidad reducida y si pertenecen al mismo ciclo o no, ambos casos resultan en distintos dominios.
        #Se debe entender que i corresponde al alumno actual y i+1 al hermano.
        
        #Mismo ciclo 1 o distinto ciclo.
        
        if (hermano[1] == "1" and i[1] == "1") or (hermano[1] != i[1]):
            
            if hermano[3] == "R" and i[3] == "R":
                
                problem.addVariable(hermano, dominio_mov_red_ciclo1)
                problem.addVariable(i, dominio_mov_red_ciclo1)
                
            elif hermano[3] == "R" and i[3] != "R":
                
                problem.addVariable(hermano, dominio_mov_red_ciclo1)
                problem.addVariable(i, dominio_ciclo1)
                
            elif hermano[3] != "R" and i[3] == "R":
                
                problem.addVariable(hermano, dominio_ciclo1)
                problem.addVariable(i, dominio_mov_red_ciclo1)
                
            else:
                
                problem.addVariable(hermano, dominio_ciclo1) 
                problem.addVariable(i, dominio_ciclo1)   
        
        #Mismo ciclo 2.
                
        elif hermano[1] == "2" and i[1] == "2":
            
            if hermano[3] == "R" and i[3] == "R":
                
                problem.addVariable(hermano, dominio_mov_red_ciclo2)
                problem.addVariable(i, dominio_mov_red_ciclo2)
                
            elif hermano[3] == "R" and i[3] != "R":
                
                problem.addVariable(hermano, dominio_mov_red_ciclo2)
                problem.addVariable(i, dominio_ciclo2)
                
            elif hermano[3] != "R" and i[3] == "R":
                
                problem.addVariable(hermano, dominio_ciclo2)
                problem.addVariable(i, dominio_mov_red_ciclo2)
                
            else:
                
                problem.addVariable(hermano, dominio_ciclo2) 
                problem.addVariable(i, dominio_ciclo2)     

    j += 1

#------------------------------------------------------------

#Funciones para restricciones.

def conflictivos(a,b):
    
    #Un alumno conflictivo no puede tener otros alumnos alrededor.
    
    #Se comprueba si los alumnos están en la misma fila, esto es la horizontal de la matriz.
    #Si la diferencia entre ambos alumnos en mayor a 1 entre los asientos de al lado, se devuelve True.
    
    if a[0] == b[0] and abs(a[1] - b[1]) > 1:
        
        return True
    
    #Se comprueba el mismo caso de la horizontal para la horizontal de arriba y de abajo. Es decir, la fila de de arriba y la de abajo al alumno conflictivo.
    
    elif (abs(a[0] - b[0]) == 1) and abs(a[1] - b[1]) > 1:
        
        return True
    
    elif abs(a[0] - b[0]) > 1:
        
        return True

def mov_reducida(a,b):
    
    #Un alumno con movilidad reducida no puede tener otros alumnos en el asiento de al lado.
    #Se comprueba que en las secciones de movilidad reducida si un asiento de una fila especifica está ocupado, el asiento de al lado no puede estar ocupado.
    
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and ((a[1] == 1 and b[1] == 2) or (a[1] == 2 and b[1] == 1)):
        
        return True
    
    elif a[0] == b[0] and abs(a[1] - b[1]) > 1:
        
        return True
        
    elif abs(a[0] - b[0]) > 1:
        
        return True

def hermanos_ciclos(a,b):  
    
    #Dos alumnos que sean hermanos deben estar sentados uno al lado del otro.
    #Esto es, tengan mismo ciclo o no según, el dominio de los hermanos será el mismo y han de estar al lado.
    #La diferencia entre uno y otro en asientos de la horizontal o fila debe ser 1.
    
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and (((a[1] != 3 and a[1] != 0) and (b[1] == 3 or b[1] == 0)) or ((a[1] != 1 and a[1] != 2) and (b[1] == 1 or b[1] == 2))):
        
        return True

def hermanos_distinto_ciclo(a,b):
    
    #Dos alumnos que sean hermanos deben estar sentados uno al lado del otro. En este caso, 'a' es el hermano menor y 'b' el mayor.
    #Al ser de distintos ciclos, el hermano mayor debe tener el dominio de los pasillos del ciclo 1.
    
    if a[0] == b[0] and abs(a[1] - b[1]) == 1 and ((a[1] != 1 and a[1] != 2) and (b[1] == 1 or b[1] == 2)):
        
        return True
#------------------------------------------------------------

#Se añaden las restricciones al problema.

#Movilidad reducida.

#Se añaden las restricciones de movilidad reducida para los alumnos que la tengan según su ciclo.

todos_conflictivos = alumnos_conflictivos + alumnos_mov_reducida_conflictivos
todos_mov_reducida = alumnos_mov_reducida + alumnos_mov_reducida_conflictivos
     
#------------------------------------------------------------

#Para una mayor facilidad en las constraints se añadiran los alumnos que son hermanos a las listas según sus características.

for i in alumnos_hermanos:
    
    if i[3] == "R":
        
        if i[2] == "C":
            
            todos_mov_reducida.append(i)
            todos_conflictivos.append(i)
            
        else:
            
            todos_mov_reducida.append(i)
            
    elif i[2] == "C":
        
        todos_conflictivos.append(i)

#Una vez se añadan se comprueba los alumnos conflictivos con los alumnos conflictivos.
#Si dos alumnos son hermanos en este caso se ignora y se pasa al siguiente.

for i in todos_conflictivos:
    
    for j in todos_conflictivos:
        
        if i != j:
            
            if i[4] != j[0]:
            
                problem.addConstraint(conflictivos, (i,j))  
            
            else:
            
                pass 
                
        else:
            
            pass 

#Se comprueba los alumnos conflictivos con los alumnos de movilidad reducida.
#Si son hermanos han de comprobarse puesto que uno de ellos es de movilidad reducida y el otro debe respectar el espacio.
            
for i in todos_conflictivos:
    
    for j in todos_mov_reducida:
        
        if i != j:
       
            problem.addConstraint(conflictivos, (i,j))
            
        else:
            
            pass 

#Se comprueba los alumnos de movilidad reducida con los alumnos de movilidad reducida.
#Al igual que en el anterior caso, si son hermanos se comprueba que uno de ellos es de movilidad reducida y el otro debe respetar el espacio.
            
for i in todos_mov_reducida:
    
    for j in todos_mov_reducida:
        
        if i != j:
            
            problem.addConstraint(mov_reducida, (i,j))
            
        else:
            
                pass 

#Se comprueba los alumnos de movilidad reducida con los alumnos comunes y que deben dejar el espacio necesario, también entre hermanos.
                        
for i in todos_mov_reducida:
    
    for j in alumnos_comunes:
            
        problem.addConstraint(mov_reducida, (i,j))

#Entre si los hermanos se comprueba su ciclo y las restricciones de hermanos en cuanto a los ciclos.
#Se tiene en cuenta las características de los hermanos y se añaden las constraints según estas.
#Los únicos que darían problemas son los de movilidad reducida.

for i in alumnos_hermanos:
    
    index_hermano = int(i[4]) - 1
    alumno_hermano = alumnos_bus[index_hermano]
    
    if i[3] == "R" or alumno_hermano[3] == "R" or (i[3] == "R" and alumno_hermano[3] == "R"):
    
        pass
    
    else:
        
        if i[1] != alumno_hermano[1]:
            
            if int(i[1]) < int(alumno_hermano[1]):
            
                problem.addConstraint(hermanos_distinto_ciclo, (i, alumno_hermano))
                
            else:
                
                problem.addConstraint(hermanos_distinto_ciclo, (alumno_hermano, i))
                
        if i[1] == alumno_hermano[1]:
            
            problem.addConstraint(hermanos_ciclos, (i, alumno_hermano))        

#Se comprueba que los alumnos no tengan un mismo asiento asignado.
                                
problem.addConstraint(AllDifferentConstraint())

#------------------------------------------------------------

#Conseguir las soluciones.

soluciones = problem.getSolutions()
n_soluciones = len(soluciones)
text_solution = {}

#print(soluciones)
print(n_soluciones)

if n_soluciones == 0:
    
    text_solution = "No hay soluciones posibles."
    
else:
#Solución aleatoria.
        
    solucion = random.choice(soluciones)

#Imprimir las soluciones en un archivo de texto con extensión '.output', inversión de la matriz.
#Se crea un diccionario con los alumnos y su posición en el autobus.

    for i in range(len(alumnos_bus)):
        
        alumno = str(alumnos_bus[i][0] + alumnos_bus[i][3] + alumnos_bus[i][2])
        for key, value in solucion.items(): 
            
            alumnos_sol = str(key[0] + key[3] + key[2])
            if alumno == alumnos_sol:
                
                position = value[0]*4 + value[1] + 1
                text_solution[alumno] = position

#------------------------------------------------------------

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
        