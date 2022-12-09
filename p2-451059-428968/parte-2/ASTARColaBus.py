#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------

import csv
import time
from Node import Node

#Lectura del fichero de entrada.

data = input("Introduce el nombre del fichero de datos: ")
data.replace(".txt", ".csv")

file = open(data, "r")
alumnos_bus = list(csv.reader(file, delimiter=","))
file.close()

#Se obtiene la solución al problema de la parte anterior
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

#[['3XX', '11'], ['1CX', '12'], ['6XX', '15'], ['5XX', '16'], ['8XR', '18'], ['4CR', '20'], ['2XX', '31'], ['7CX', '32']]

#------------------------------------------------------------
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

def calculateAllCost (node, cola_ordenada):
    
    gcost = 0
    addedNode = node.state
    for i in range(len(addedNode)):
        
        if addedNode[i][1] == "X" and addedNode[i][2] == "X":
            
            if addedNode[i-1][1] == "X" and addedNode[i-1][2] == "R":
                
                gcost = 0
                
            else:
                
                gcost += 1
            
    return gcost

#------------------------------------------------------------

def calculateGCost (node, parent, cola_ordenada):
    
    addedNode = node.state
    countConflicts = 0
    
    for i in range(len(addedNode)):
        
        if addedNode[i][1] == "C":
            
            countConflicts += 1
            
    if countConflicts >= 1:
        
        return calculateAllCost(node, cola_ordenada)
    
    if len(parent.state) == 0:
        
        addedNode = addedNode[-1]
        addedNode = addedNode[2]
        
        if addedNode == "R":
            
            gcost = 3
            
        else:
            
            gcost = 1
        
    nodeParent = parent.state
    nodeParent = nodeParent[-1]
    nodeParent = str(nodeParent[1] + nodeParent[2])
    
    addedNode = addedNode[-1]
    addedNode = str(addedNode[1] + addedNode[2])
    
    if nodeParent == "XX" and addedNode == "XX":
        
        gcost = parent.gCost + 1
        
    elif nodeParent == "XX" and addedNode == "XR":
        
        gcost = parent.gCost + 3
        
    elif nodeParent == "XR" and addedNode == "XX":
        
        gcost = parent.gCost + 0 
    
    return gcost
        
    
#------------------------------------------------------------

def calculateHCost (node, heuristic, cola_ordenada):
    
    if heuristic == 1:
        
        hcost = len(cola_ordenada) - len(node.state)
        
        if hcost == 0:
            
            return hcost, True
        
        return hcost, False
    
#------------------------------------------------------------

#Calcular el valor del nodo expandido

def caculateNodeCosts(node, parent, heuristic, cola_ordenada):
    
    node.parent = parent
    node.gCost = calculateGCost(node, parent, cola_ordenada)
    node.hCost, goal = calculateHCost(node, heuristic, cola_ordenada)
    node.fCost = node.gCost + node.hCost
    return node, goal

#------------------------------------------------------------

#Sort de los nodos según su valor fCost

def orderOpenList (openList):
    
    costList = []
    for i in range(len(openList)):
        
        costList.append(openList[i].fCost)
    
    costList.sort()
    newOpenList = []
    while len(costList) > 0:
        
        for i in range(len(openList)):
            
            if openList[i].fCost == costList[0]:
                
                newOpenList.append(openList[i])
                costList.pop(0)
                
                break

    return newOpenList
#------------------------------------------------------------

#Creación de hijos de un nodo

def nodeChildren(lista_tomar, lista_poner, expandedNode, heuristic):
    
    for i in range(len(lista_tomar)):
        
        expansionNode = expandedNode.state
        
        if lista_tomar[i][0] not in expansionNode:
            
            addedAlumno = lista_tomar[i][0]
            checkLast = expansionNode[-1]
            
            if checkLast[2] == "R" and addedAlumno[2] == "R":
                
                pass
            
            if addedAlumno[2] == "R" and (len(expansionNode) == (len(lista_tomar) - 1)):
                
                pass
            
            expansionNode.append(lista_tomar[i][0])
            node = Node()
            node.state = expansionNode
            node.parent = expandedNode
            node, goal = caculateNodeCosts(node, expandedNode, heuristic, lista_tomar)
            lista_poner.append(node)
        
    lista_poner = orderOpenList(lista_poner)
        
    return lista_poner, goal
        
#------------------------------------------------------------

#Busqueda del nodo objetivo

def searchGoalNode (lista, longitud_estado):
    
    for i in range(len(lista)):
        
        if len(lista[i].state) == longitud_estado:
            
            return lista[i]
            

#------------------------------------------------------------

#Transformación del estado meta en diccionario como resultado
    
def transformGoalNode (node, lista_alumnos): 
       
    goalNode = {}
    for i in range(len(node.state)):
        
        for j in range(len(lista_alumnos)):
            
            if node.state[i] == lista_alumnos[j][0]:
                
                goalNode[str(node.state[i])] = lista_alumnos[j][1]
        
    return goalNode    

#------------------------------------------------------------
def AStarAlgorithm (cola_ordenada, heuristic):
    
    lenCola = len(cola_ordenada)
    
    startNode = Node()
    startNode = Node.state = []
    startNode.gCost = startNode.hCost = startNode.fCost = 0
    
    openList = []
    closedList = []
    goalReached = False
    openList.append(startNode)
    
    while len(openList) > 0 and not goalReached:
        
        expanded = openList.pop(0)
        
        if expanded in closedList:
            
            continue
        
        else:
            
            closedList.append(expanded)
            
        if expanded.state == []:
            
            openList, goalReached = nodeChildren(cola_ordenada, openList, expanded, heuristic)
        
        openList, goalReached = nodeChildren(cola_ordenada, openList, expanded, heuristic)
        
    expandedNodeGoal = searchGoalNode(openList, lenCola) 
        
    return expandedNodeGoal, expandedNodeGoal.fCost ,len(closedList)     
        
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
