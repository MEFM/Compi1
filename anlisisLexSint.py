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
    global tominTokens,contador, columna, fila, simbolos, tokens, validador, validadorOperacion, erroresSintx

    listaTokens = []
    envioTOk = []
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


            #listaTokens.append([fila, columna, "Salto","Salto"])
            
            tokens = listaTokens

            tokens.append([fila+1,columna+1,"$$$","Final"])

            sintaxis()

            if validadorOperacion == False:
                erroresSintx.append([fila, columna, validadorOperacion])
            else:
                erroresSintx.append([fila, columna, validadorOperacion])
            
            listaTokens = []
            columna = 0
            fila += 1
            contador += 1
    
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
    
    #listaTokens.append([fila+1,columna+1,"$$$","Final"])

    tokens = listaTokens
    
    for token in tokens:
        print(token)

    reporte(texto)
    #sintaxis()
    
    



    
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
    global tokens, cabeza,validadorOperacion,timonTokens
    print("Sintaxis")
    timonTokens = 0
    validadorOperacion = False
    #Inicio analizador sintactico
    cabeza = tokens[0]
    A()

    if cabeza[2] != "$$$":
        validadorOperacion = True
    else:
        validadorOperacion = False
def posiblesErrores(tipo):
    global validadorOperacion

    validadorOperacion = True
    
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
    
    
    

def encaje(tokenss):  
    global cabeza, timonTokens, tokens, validadorOperacion

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

    linea = texto.split("\n")
    '''
    for token in erroresSintx:
        print("Expersion ",linea[token[0]],token[2])
    '''
    with open("/home/Operacions.html","w+") as file:

        file.seek(0,0)

        file.write("<html>")
        file.write("<head>")
        file.write("<title>Reporte de Archivo RMT</title>")
        file.write("<style type=\"text/css\">table{table-layout: fixed; width: 100%; border-collapse: collapse;}</style>")
        file.write("</head>")
        file.write("<body>")
        file.write("<h1>Tabla De Confirmacion RMT</h1>")
        file.write("<table summary=\"Operaciones Econtradas\">")
        file.write("<caption>Operaciones encontradas en el archivo de entrada</caption>")

        file.write("<thead>")


        file.write("<tr>")
        file.write("<th scope=\"col\">No.</th>")
        file.write("<th>Columna</th>")
        file.write("<th>File</th>")
        file.write("<th>Operacion</th>")
        file.write("<th>Validacion</th>")
        file.write("</tr>")


        file.write("</thead>")


        file.write("<tbody>")
        file.write("</tbody>")
        cont = 1
        for error in erroresSintx:
            file.write("<tr>")
            file.write("<th scope=\"row\">"+str(cont)+"</th>")
            file.write("<th scope=\"row\"> "+str(error[0])+"</th>")
            file.write("<th scope=\"row\">"+str(error[1])+"</th>")
            file.write("<th scope=\"row\">"+linea[error[0]]+"</th>")
            if error[2] == True:                
                file.write("<th scope=\"row\">Incorrecto</th>")
            else:
                file.write("<th scope=\"row\">Correcto</th>")                
            file.write("</tr>")

            cont += 1

        file.write("</table>")
        file.write("</body>")
        file.write("</html>")

        file.close()

    webbrowser.open("/home/Operaciones.html")