from Type import Type
import Hojas
import TabNext
import json

class nodo:

    #Entrada a identificar que es cada cosa
    def __init__(self, lexema, tipo, numero, izquierda, derecha):
        self.first = []
        self.last = []
        self.anul = True

        self.lex = lexema
        self.type = tipo
        self.num = numero

        self.acept = False



        if lexema == "#":
            self.acept = True

        self.izquierda = izquierda
        self.derecha = derecha


    def getNod(self):

        izquierda = self.izquierda.getNod() if isinstance(self.izquierda, nodo) else None
        derecha = self.derecha.getNod() if isinstance(self.derecha, nodo) else None
    

        if self.type == Type.Hoja:
            self.anul = False
            self.first.append(self.num)
            self.last.append(self.num)
        elif self.type == Type.And:

            if (isinstance(izquierda,nodo) and isinstance(derecha,nodo)):
                self.anul = izquierda.anul and derecha.anul

                if izquierda.anul:
                    self.first.extend(izquierda.first)
                    self.first.extend(derecha.first)
                else:
                    self.first.extend(izquierda.first)

                if derecha.anul:
                    self.last.extend(izquierda.last)
                    self.last.extend(derecha.last)
                else:
                    self.last.extend(derecha.last)

        elif self.type == Type.Or:
            
            if (isinstance(izquierda, nodo) and isinstance(derecha,nodo)):
                self.anul = izquierda.anul or derecha.anul

                self.first.extend(izquierda.first)
                self.first.extend(derecha.first)

                self.last.extend(izquierda.last)
                self.last.extend(derecha.last)                    

        elif self.type == Type.Kleene:
            if isinstance(izquierda, nodo):
                self.anul = True
                self.first.extend(izquierda.first)
                self.last.extend(izquierda.last)

        elif self.type == Type.Interr:
            if isinstance(izquierda, nodo):
                self.anul = True
                self.first.extend(izquierda.first)
                self.last.extend(izquierda.last)

                pass
        
        else:
            pass

        return self


    def next(self):
        izquierda = None if (self.izquierda == None)else self.izquierda.next()
        derecha = None if (self.derecha == None) else self.derecha.next()

        if self.type == Type.And:
            for i in izquierda.last: 
                nodo = Hojas.getHoja(i)
                TabNext.append(nodo.num, nodo.lex,derecha.first)
                
        elif self.type == Type.Kleene:
            for i in izquierda.last:
                nodo = Hojas.getHoja(i)
                TabNext.append(nodo.num, nodo.lex,izquierda.first)
        else:
            pass
        return self 