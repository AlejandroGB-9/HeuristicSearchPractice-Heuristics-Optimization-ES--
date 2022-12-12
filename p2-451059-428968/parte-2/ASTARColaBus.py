#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------

import csv
import time
from Node import Node
import sys

#Lectura del fichero de entrada.
#El fichero de entrada se toma como argumento de la terminal al ejecutar el programa por esta.

data = sys.argv[1]
data.replace(".txt", ".csv")

#Se lee el fichero de entrada y se almacena en una lista de listas.
file = open(data, "r")
alumnos_bus = list(csv.reader(file, delimiter=","))
file.close()

#Se obtiene la solución al problema de la parte anterior y se transforma el diccionario en el siguiente formato.
#[['3XX', '11'], ['1CX', '12'], ['6XX', '15'], ['5XX', '16'], ['8XR', '18'], ['4CR', '20'], ['2XX', '31'], ['7CX', '32']]

alumnos_bus = alumnos_bus[1]
for i in range(len(alumnos_bus)):
    
    alumnos_bus[i] = alumnos_bus[i].split(" ")
    
for i in range(len(alumnos_bus)):
    
    if len(alumnos_bus[i]) == 3:
        
        alumnos_bus[i].pop(0)
        
    for j in range(len(alumnos_bus[i])):
        
        if len(alumnos_bus[i][j]) == 0:
            
            alumnos_bus[i].pop(j)
            
        else:
            
            alumnos_bus[i][j] = str(alumnos_bus[i][j]) 
            inicio = alumnos_bus[i][j]
            
            if inicio[0] == "{":
                
                inicio = inicio.replace("{", "")
                
            if inicio[-1] == ":":
                
                inicio = inicio.replace(":", "")
                
            if inicio[-1] == "}":
                
                inicio = inicio.replace("}", "")
    
            alumnos_bus[i][j] = inicio

#------------------------------------------------------------

#Se ordena la lista de alumnos por el número de asiento obtenido en la parte anterior. De menor a mayor.

def orderListAlumnos (lista):
    
    temp = 0
    for i in range(len(lista)):
        
        temp = lista[i][1]
        lista[i][1] = lista[i][0]
        lista[i][0] = temp
        
    lista.sort()
    
    for i in range(len(lista)):
        
        temp = lista[i][1]
        lista[i][1] = lista[i][0]
        lista[i][0] = temp
        
    return lista

#------------------------------------------------------------

#Función para calcular el coste de un nodo si presenta alumnos conflictivos.
#Es una función recursiva que recorre el nodo y calcula el coste de cada alumno en la cola según los siguientes casos.
#Se recuerda que el coste de un alumno a subir a uno con movilidad reducida es de 3.
#Un alumno común cuesta 1.
#Un alumno conflictivo cuesta 1 pero duplica el coste de los que se encuentren delante y atrás de él.
#TODO: Se tiene que implementar el último punto de los conflictivos, con el que se necesita la cola_ordenada.

def calculateAllCost (node, cola_ordenada):
    
    gcost = 0
    addedNode = node.state
    for i in range(len(addedNode)):
        
        #Para los siguientes casos se calcula el coste de un alumno en la cola.
        #Se representan estas condiciones con una lista para entender cada condición.
        #Formato de la lista: [abuelo, padre, nodo, hijo]
        
        if addedNode[i][1] == "X" and addedNode[i][2] == "X":
            
            if addedNode[i-1][1] == "X" and addedNode[i-1][2] == "R":
                
                if addedNode[i-2][1] == "C":
                    
                    #[C#, XR, XX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2
                        
                    else:
                        
                        #[C#, XR, XX, ##]
                        gcost += 3*2
                        
                else:
                    
                    #[##, XR, XX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2
                        
                    else:
                        
                        #[##, XR, XX, ##]
                        gcost += 3
                
            elif addedNode[i-1][1] == "C" and addedNode[i-1][2] == "X":
                
                #[##, CX, XX, C#]
                if addedNode[i+1][1] == "C":
                    
                    gcost += 1*2*2
                    
                else:
                    
                    #[##, CX, XX, ##]
                    gcost += 1*2
                    
            elif addedNode[i-1][1] == "C" and addedNode[i-1][2] == "R":
                
                if addedNode[i-2][1] == "C":
                    
                    #[C#, CR, XX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2*2
                        
                    else:
                        
                        #[C#, CR, XX, ##]
                        gcost += 3*2*2
                        
                else:
                    
                    #[##, CR, XX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2
                        
                    else:
                        
                        #[##, CR, XX, ##]
                        gcost += 3*2
                    
            elif addedNode[i-1][1] == "X" and addedNode[i-1][2] == "X":
                
                #[##, XX, XX, C#]
                if addedNode[i+1][1] == "C":
                    
                    gcost += 1*2
                    
                else:
                    
                    #[##, XX, XX, ##]
                    gcost += 1
                    
        if addedNode[i][1] == "C" and addedNode[i][2] == "X":
            
            if addedNode[i-1][1] == "X" and addedNode[i-1][2] == "R":
                
                if addedNode[i-2][1] == "C":
                    
                    #[C#, XR, CX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2*2
                        
                    else:
                        
                        #[C#, XR, CX, ##]
                        gcost += 3*2*2
                        
                else:
                    
                    #[##, XR, CX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2
                        
                    else:
                        
                        #[##, XR, CX, ##]
                        gcost += 3*2
                
            elif addedNode[i-1][1] == "C" and addedNode[i-1][2] == "X":
                
                #[##, CX, CX, C#]
                if addedNode[i+1][1] == "C":
                    
                    gcost += 1*2*2
                    
                else:
                    
                    #[##, CX, CX, ##]
                    gcost += 1*2
                    
            elif addedNode[i-1][1] == "C" and addedNode[i-1][2] == "R":
                
                if addedNode[i-2][1] == "C":
                    
                    #[C#, CR, CX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2*2*2
                        
                    else:
                        
                        #[C#, CR, CX, ##]
                        gcost += 3*2*2*2
                        
                else:
                    
                    #[##, CR, CX, C#]
                    if addedNode[i+1][1] == "C":
                        
                        gcost += 3*2*2*2
                        
                    else:
                        
                        #[##, CR, CX, ##]
                        gcost += 3*2*2
                    
            elif addedNode[i-1][1] == "X" and addedNode[i-1][2] == "X":
                
                #[##, XX, CX, C#]
                if addedNode[i+1][1] == "C":
                    
                    gcost += 1*2
                    
                else:
                    
                    #[##, XX, CX, ##]
                    gcost += 1
            
    return gcost

#------------------------------------------------------------

#Función para calcular el coste g de un nodo.

def calculateGCost (node, parent, cola_ordenada):
    
    addedNode = node.state
    countConflicts = 0
    gcost = 0
    
    #Se calcula cuantos conflictos hay en la cola.
    
    for i in range(len(addedNode)):
        
        if addedNode[i][1] == "C":
            
            countConflicts += 1
            
    #En el caso de haber conflictivos, se calcula el coste g de la cola con una función externa al ser un caso especial.        
    if countConflicts >= 1:
        
        return calculateAllCost(node, cola_ordenada)
    
    #En caso contrario, se calcula el coste g de la cola de una forma más sencilla.
    
    #Si el nodo añadido es el primer alumno que se introduce en la cola.
    
    if len(parent.state) == 0:
        
        addedNode = addedNode[-1]
        addedNode = addedNode[2]
        
        if addedNode == "R":
            
            #La razón por la que es cero es porque el tiempo de subir es la del alumno con movilidad reducida y otro alumno.
            #El coste se aplicará al alumno que lo ayude a subir.
             
            gcost = 0
            
        else:
            
            #En caso de ser un alumno común el coste es 1.
            
            gcost = 1
    
    #En el caso de que tenga un padre.
    #Se mira que alumno era antes de añadido por si se da el caso de ser de movilidad reducida.
    #Según el caso se calcula el coste g en base a los coste mencionados anteriormente y el coste del padre.
        
    nodeParent = parent.state
    nodeParent = nodeParent[-1]
    nodeParent = str(nodeParent[1] + nodeParent[2])
    
    addedNode = addedNode[-1]
    addedNode = str(addedNode[1] + addedNode[2])
    
    if nodeParent == "XX" and addedNode == "XX":
        
        gcost = parent.gCost + 1
        
    elif nodeParent == "XX" and addedNode == "XR":
        
        gcost = parent.gCost + 0
        
    elif nodeParent == "XR" and addedNode == "XX":
        
        gcost = parent.gCost + 3 
    
    #Se devuelve el coste g.
    
    return gcost
        
    
#------------------------------------------------------------

#Función para calcular el coste heurístico de un nodo.
#Se recibe el nodo, la heurística a utilizar y la cola ordenada en caso de que se elija la heur == 1.

def calculateHCost (node, heuristic, cola_ordenada):
    
    #Si la heurística es 1, esta es cuantos asientos siguen estando libres hasta alcanzar la última posición de la cola.	
    
    hcost = 0
    
    if heuristic == 1:
        
        #Se calcula el coste heurístico con la longitud que tenga la cola inicial de alumnos - la longitud del nodo.
        hcost = len(cola_ordenada) - len(node.state)
        
        #En caso de ser el coste cero, se ha alcanzado el objetivo.
        if hcost == 0:
            
            #Se devuelve el coste heurístico y True para indicar que se ha alcanzado el nodo meta.
            return hcost, True
        
        #En caso contrario, se devuelve el coste heurístico y False para indicar que no se ha alcanzado el nodo meta.
        return hcost, False
    
#------------------------------------------------------------

#Calcular el valor del nodo expandido.
#Es necesario el uso de funciones externas para los costes g y h, estas funciones son las anteriores.

def caculateNodeCosts(node, parent, heuristic, cola_ordenada):
    
    node.gCost = calculateGCost(node, parent, cola_ordenada)
    node.hCost, goal = calculateHCost(node, heuristic, cola_ordenada)
    
    #Se devuelve el nodo hijo con sus costes y si se ha alcanzado el nodo meta.
    
    return node, goal

#------------------------------------------------------------

#Sort de los nodos según su valor fCost
#Es decir, una función que ordena la openList una vez añadido los hijos a esta lista.
#Se ordenan los hijos segúm su coste de menor a mayor.

def orderOpenList (openList):
    
    #Se crea una lista con los costes f de los nodos de la openList y se ordena.
    
    costList = []
    for i in range(len(openList)):
        
        costList.append(openList[i].fCost)
    
    costList.sort()
    newOpenList = []
    
    #Según los costes se colocan los nodos según su coste f.
    
    while len(costList) > 0:
        
        for i in range(len(openList)):
            
            if openList[i].fCost == costList[0]:
                
                newOpenList.append(openList[i])
                costList.pop(0)
                
                break

    #Se devuelve la openList ordenada.       
                
    return newOpenList
#------------------------------------------------------------

#Creación de hijos de un nodo

def nodeChildren(lista_tomar, lista_poner, expandedNode, heuristic):
    
    goal = False
    
    for i in range(len(lista_tomar)):
        
        expansionNode = expandedNode.state
        
        #Se añaden los alumnos al nodo expandido que no se encuentren en el nodo expandido.
        #Así se genera los nodos hijos 
        
        if lista_tomar[i][0] not in expansionNode:
            
            if len(expansionNode) == 0:
                
                expansionNode.append(lista_tomar[i][0])
                node = Node(expansionNode, expandedNode, 0, 0)
                node, goal = caculateNodeCosts(node, expandedNode, heuristic, lista_tomar)
                lista_poner.append(node)
                
            else:
                
                addedAlumno = lista_tomar[i][0]
                checkLast = expansionNode[-1]
                
                #Se comprueba que los hijos cumplen las normas.
                #Si el alumno anterior es de movilidad reducida y el alumno añadido es de movilidad reducida no se añade.
                
                if checkLast[2] == "R" and addedAlumno[2] == "R":
                    
                    pass
                
                #Si el añadido es de movilidad reducida y el nodo expandido tiene la longitud de la cola inicial - 1, no se añade.
                
                elif addedAlumno[2] == "R" and (len(expansionNode) == (len(lista_tomar) - 1)):
                    
                    pass
                
                else:
                    
                    #En caso contrario, se añade el alumno al nodo expandido y se crea el nodo hijo.
                    #Se añade como un nodo con su padre y se calculan sus costes.
                    #Finalmente se añade a la openList.
                    
                    expansionNode.append(lista_tomar[i][0])
                    node = Node(expansionNode, expandedNode, 0, 0)
                    node, goal = caculateNodeCosts(node, expandedNode, heuristic, lista_tomar)
                    lista_poner.append(node)
    
    #Se ordena y se devuelve la openList con los hijos añadidos y si se ha llegado al nodo meta.
        
    lista_poner = orderOpenList(lista_poner)
        
    return lista_poner, goal
        
#------------------------------------------------------------

#Busqueda del nodo objetivo
#Se busca el nodo objetivo en la lista de nodos por expandir al ser la openList.
#Para ello el nodo objetivo debe tener la longitud de la cola inicial.

def searchGoalNode (lista, longitud_estado):
    
    for i in range(len(lista)):
        
        if len(lista[i].state) == longitud_estado:
            
            return lista[i]
            

#------------------------------------------------------------

#Transformación del estado meta en diccionario como resultado
#Se transforma el estado meta en un diccionario con el nombre del alumno y su posición en la cola.
    
def transformGoalNode (node, lista_alumnos): 
       
    goalNode = {}
    for i in range(len(node.state)):
        
        for j in range(len(lista_alumnos)):
            
            if node.state[i] == lista_alumnos[j][0]:
                
                goalNode[str(node.state[i])] = lista_alumnos[j][1]
        
    return goalNode    

#------------------------------------------------------------

#Algoritmo A*
#Se crea el nodo inicial y se añade a la openList. 
#El nodo inicial es el nodo vacío o sin alumnos.

def AStarAlgorithm (cola_ordenada, heuristic):
    
    lenCola = len(cola_ordenada)
    
    startNode = Node( [], None, 0, 0 )

    
    openList = []
    closedList = []
    goalReached = False
    openList.append(startNode)
    
    #Se segurirá expandiendo nodos mientras la openList no esté vacía y no se haya llegado al nodo meta.
    
    while len(openList) > 0 and not goalReached:
        
        expanded = openList.pop(0)
        
        #Si el nodo expandido ya se encuentra en la closedList, se ignora.
        
        if expanded in closedList:
            
            continue
        
        else:
            
            closedList.append(expanded)
            openList, goalReached = nodeChildren(cola_ordenada, openList, expanded, heuristic)    
    
    #Una vez alcanzado el nodo meta, se devuelve el nodo meta, su coste y el número de nodos expandidos.
        
    expandedNodeGoal = searchGoalNode(openList, lenCola)
    expandedNodes = len(closedList) + len(openList) 
        
    return expandedNodeGoal, expandedNodeGoal.fCost ,expandedNodes     
        
#------------------------------------------------------------

#Sort de la lista de alumnos según el asiento que tengan

orderListAlumnos(alumnos_bus)

#Llamada al algoritmo A* y comienzo del contador de tiempo

start_time = time.time()
resultado, costeNodoMeta ,nodosExpandidos = AStarAlgorithm(alumnos_bus, 1)
end_time = time.time() + start_time
#Creamos el diccionario con el resultado de la cola de alumnos

colaAlumnos = transformGoalNode(resultado, alumnos_bus)

#Creamos el archivo de salida

data.replace(".txt", ".output")
file_output = open(data, "w")
file_output.seek(0)
file_output.truncate()
file_output.write("Tiempo total: " + str(end_time))
file_output.write("Coste total: " + str(costeNodoMeta))
file_output.write("Longitud del plan: " + str(4)) #TODO: Calcular la longitud del plan
file_output.write("Nodos expandidos: " + str(nodosExpandidos))
file_output.write(colaAlumnos)
file_output.close()
