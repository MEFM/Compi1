import re
import webbrowser
import os

#Analizador lexico
contador = 0
columna = 0
fila = 0
validador = False

simbolos = {"ParAp":"(", "ParC":")","Ast":"*","Sum":"+","Rest":"-","Div":"/","Punto":"."}
tokens = []
erroresL = []

#Analizador sintactico

erroresSintx = []
cabeza = []
timonTokens = 0
validadorOperacion = False


def analisisLex(texto):
    global contador, columna, fila, simbolos, tokens, validador, validadorOperacion

    listaTokens = []

    while contador < len(texto):
        if re.search("[A-Za-z]", texto[contador]):
            listaTokens.append(Identificador(fila, columna, texto, texto[contador]))
        elif re.search(r"[0-9]", texto[contador]):
            listaTokens.append(Numero(fila, columna, texto, texto[contador]))
        elif re.search("[ \t]",texto[contador]):

            columna += 1
            contador += 1
            pass
        elif re.search("[\n]",texto[contador]):
            columna = 0
            fila += 1
            contador += 1
            tokens = listaTokens
            listaTokens.append([fila+1,columna+1,"$$$","Final"])
            sintaxis()
            if validadorOperacion == False:
                erroresSintx.append([fila+1,columna+1,validadorOperacion])
            else:
                erroresSintx.append([fila+1,columna+1,validadorOperacion])

            pass        
        else:
            validadorSigno = False

            for clave in simbolos:
                valor = simbolos[clave]

                if re.search(r"["+valor+"]",texto[contador]):
                    listaTokens.append([fila, columna, clave.replace("'",""), valor.replace("//","")])
                    contador += 1
                    columna += 1
                    validadorSigno = True
                    break
            
            if validadorSigno == False:
                columna +=1
                erroresL.append([fila, columna, texto[contador], "Error lexico"])
    
    listaTokens.append([fila+1,columna+1,"$$$","Final"])

    tokens = listaTokens

    for token in tokens:
        print(token)

    sintaxis()



    
def Identificador(lineaa,columnaa, texto, palabra):
    global fila, columna, contador

    columna +=1
    contador += 1
    print("Identificador")
    if contador < len(texto):

        if re.search("[A-Za-z0-9_]",texto[contador]):
            return Identificador(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            return [lineaa, columnaa, "ID", palabra]
    else:
         return [lineaa, columna, "ID", palabra]

def Numero(lineaa, columnaa, texto, palabra):
    global contador, columna, fila, validador

    contador += 1
    columna += 1

    if contador < len(texto):
        if re.search("[0-9]",texto[contador]):

            return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            
        elif re.search("[\.]",texto[contador]):
            if validador == True:

                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            else:
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            return [lineaa, columnaa, "Numero", palabra]        
            
            
    else:
        return [lineaa, columnaa, "Numero", palabra]
    pass




def sintaxis():
    global tokens, cabeza
    print("Sintaxis")
    #Inicio analizador sintactico

    cabeza = tokens[0]
    A()

    if cabeza != "$$$":
        print("Error")

def posiblesErrores(tipo):

    if tipo == "Numero" or tipo == "ID":
        return "Falta Identificador o Numero"
    elif tipo == "ParAp":
        return "Falta parentesis de apertura"
    elif tipo == "ParC":
        return "Falta parentesis de cerradura"
    elif tipo == "Ast":
        return "Falta asterisco en la multiplicacion"
    elif tipo == "Rest":
        return "Falta guion para la resta"
    elif tipo == "Sum":
        return "Falta cruz para la suma"
    elif tipo == "Div":
        return "Falta slash para la divicion"
    else:
        return "No se encuentra "+tipo+" en el lenguaje"
    pass

def encaje(tokenss):  
    global cabeza, timonTokens, tokens

    #print("Cabeza: ",cabeza[2], " Tokenss: ",tokenss)
    
    if  (cabeza[2] != tokenss):                
        print("Error sintactico. "+posiblesErrores(tokenss))

    if cabeza[2] == "$$$":
        print("Final de analisis sintactico")
        timonTokens = 0
        tokens = []
    elif cabeza[2] != "$$$":
        timonTokens = timonTokens + 1
        cabeza = tokens[timonTokens]       

def A():
    global cabeza 
    B()
    AP()
    pass
#simbolos = {"ParAp":"(", "ParC":")","Ast":"*","Sum":"+","Rest":"-","Div":"/","Punto":"."}
def AP():
    global cabeza, timonTokens

    #envio = ["Rest","Sum","Numero","ID","ParAp","ParC","$$$"]

    if cabeza[2] == "Sum":
       encaje("Sum")
       B()
       AP()

    elif cabeza[2] == "Rest":
        encaje("Rest")
        B()
        AP()

def B():
    global cabeza
    #envio = ["Div","Ast","Rest","Sum","Numero","ID","ParAp","ParC","$$$"]
    C()
    BP()

def BP():
    global cabeza
    #envio = ["Div","Ast","Sum","Numero","ID","ParAp","ParC","$$$"]
    if cabeza[2] == "Ast":
        encaje("Ast")
        C()
        BP()
    elif cabeza[2] == "Div":
        encaje("Div")
        C()
        BP()

def C():
    global cabeza
    print("C")

    if cabeza[2].strip() == "ParAp": 
        encaje("ParAp")
        A()
        encaje("ParC")
    elif cabeza[2] == "Numero":
        encaje("Numero")
    elif cabeza[2] == "ID":
        encaje("ID")
    

def reporte(texto):
    global erroresSintx
    