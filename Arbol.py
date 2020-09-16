from HojaNo import numHoja
from Nodo import nodo
from Type import Type
import Hojas

class constArbol:

    def __init__(self, er): #er: Expresion regular

        nh = numHoja(er) 
        self.pila = []

        for x in reversed(list(er)):

            if x == "|":
                izq = self.pila.pop(len(self.pila) - 1)
                der = self.pila.pop(len(self.pila) - 1)

                if (isinstance(izq,nodo) and isinstance(der,nodo)):
                    n = nodo(x, Type.Or, 0, izq, der)
                    self.pila.append(n)

            elif x == ".":
                izq = self.pila.pop(len(self.pila) - 1)
                der = self.pila.pop(len(self.pila) - 1)

                if (isinstance(izq,nodo) and isinstance(der,nodo)):
                    n = nodo(x, Type.And, 0, izq, der)
                    self.pila.append(n)
            
            elif x == "*":
                unario = self.pila.pop(len(self.pila) - 1)

                if (isinstance(unario,nodo)):
                    n = nodo(x, Type.Kleene, 0, unario, None)
                    self.pila.append(n)

            elif x == "?":
                unario = self.pila.pop(len(self.pila) - 1)
                if (isinstance(unario, nodo)):
                    n = nodo(x, Type.Interr, 0, unario, None)
                    self.pila.append(n)
                
            else:
                n = nodo(x, Type.Hoja, nh.getNum(), None, None)
                self.pila.append(n)
                Hojas.addHoja(n) # Importante agregar la hoja


        self.root = self.pila.pop(len(self.pila)-1)


    def getRoot(self):
        return self.root