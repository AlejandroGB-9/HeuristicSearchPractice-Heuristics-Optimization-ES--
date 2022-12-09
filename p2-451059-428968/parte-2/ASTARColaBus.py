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

#Calcular el valor del nodo expandido

def caculateNodeCosts(node, parent):
    node.parent = parent
    node.gCost = parent.gCost + 1
    #TODO: Calcular el valor de hCost
    if node.state[0] == "X":
        node.hCost = 1
    node.hCost = 0
    node.fCost = node.gCost + node.hCost
    return node

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

#Creación de hijos
#TODO: Poner padres a los nodos hijos

def nodeChildren(lista_tomar, lista_poner):
    newList = []
    for i in range(len(lista_tomar)):
        node = Node()
        node.state = lista_tomar[i]
        newList.append(node)
        
    for i in range(len(newList)):
        lista_poner.append(newList[i])
        
    return lista_poner
        
#------------------------------------------------------------

#Busqueda del nodo objetivo

def searchGoalNode (lista, longitud_estado):
    lista = orderOpenList(lista)
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
def AStarAlgorithm (cola_ordenada):
    startNode = Node()
    startNode = Node.state = []
    startNode.gCost = startNode.hCost = startNode.fCost = 0
    
    openList = []
    closedList = []
    openList.append(startNode)
    while len(openList) > 0:
        expanded = openList.pop(0)
        closedList.append(expanded)
        if expanded in closedList:
            continue
        if expanded.state == []:
            openList = nodeChildren(cola_ordenada, openList)
        
        openList = nodeChildren(openList, openList)
        
    longitud_estado = len(cola_ordenada)
    expandedNodes = searchGoalNode(closedList, longitud_estado) 
        
    return expandedNodes, expandedNodes.fCost ,len(closedList)     
        
#------------------------------------------------------------

#Sort de la lista de alumnos según el asiento que tengan

orderListAlumnos(alumnos_bus)

#Llamada al algoritmo A* y comienzo del contador de tiempo

start_time = time.time()
resultado, costeNodoMeta ,nodosExpandidos = AStarAlgorithm(alumnos_bus)
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
