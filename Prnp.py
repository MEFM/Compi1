from Arbol import constArbol
from TransitionTab import tranTab
import json
import Transition
import TabNext

class Principal:

    def __init__(self, ER, nombre):
        
        ca = constArbol(ER)
        raiz = ca.getRoot()

        raiz.getNod()
        raiz.next()
        tran = tranTab(raiz)
        tran.grafo(nombre)



