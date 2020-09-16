from Transition import transicion
from graphviz import Digraph
from Nodo import nodo
import TabNext
import Hojas

class tranTab:

    def __init__(self, root):
        self.states = []
        self.contador = 0


        self.states.append( ["S"+str(self.contador), root.first, [], False] )
        self.contador += 1

        for estado in self.states:
            elementos = estado[1]
 
            for hoja in elementos:

                lexema, siguientes = TabNext.getSig(hoja)

                estado_existe = False
                estado_encontadorrado = ""
                for e in self.states:
                    if "".join(str(v) for v in e[1]) == "".join(str(v) for v in siguientes):
                        estado_existe = True
                        estado_encontadorrado = e[0]
                        break


                if not estado_existe:
                    if Hojas.aceptacion(hoja):
                        estado[3] = True
                    
                    if lexema == "":
                        continue

                    nuevo = ["S"+str(self.contador), siguientes, [], False]
                    trans = transicion(estado[0], lexema, nuevo[0])
                    estado[2].append(trans)

                    self.contador += 1
                    self.states.append(nuevo)

                else:
                    if Hojas.aceptacion(hoja):
                        estado[3] = True
                    
                    trans_existe = False

                    for trans in estado[2]:
                        if trans.comp(estado[0], lexema):
                            trans_existe = True
                            break

                    if not trans_existe:
                        trans = transicion(estado[0], lexema, estado_encontadorrado)
                        estado[2].append(trans)


    def grafo(self, nombre=""):
        dot = Digraph(comment='Grafica de states')
        dot.attr('node', shape='circle')
        dot.node("L: Letras\\nD: Digitos\\nS: Slash\\nT: Todo\\nA: Asterisco\\nI: Salto\\nC: Comilla\\nK: Simbolo\\nP: Punto")
        for e in self.states:
            dot.node(e[0],e[0])
            if e[3]:
                dot.node(e[0], shape='doublecircle')

        
        for e in self.states:
            for t in e[2]:
                dot.edge(t.eIni, t.eFin, label=t.tran)


        dot.render(nombre+".gv",view=True)
        
                    

