import re
from Prnp import *
import os
import webbrowser
#########################################################################################################

###################################-ANALIZADOR JAVA SCRIPT-###################################

#########################################################################################################

#Banderas de expresiones

banderaID = False
banderaNum = False
banderaComntL = False
banderaComntML = False
banderaCadena = False
banderaSigno = False
banderaChr = False

#Contador expresiones encontradas


#Bandera Especial para numeros 
validador = False


#Contadores de texto
linea = 0
columna = 0
contador = 0

textoLimpio = ""

Errores = []
tokens = []

palabrasReservadas = ["console","var","if","for","while","do","continue","break","else","return","function","constructor","class","Math","pow","switch","case","new","alert","try","catch","in","this","log"]
boolNum = ["true","false"]
simbolos = {"ParAp":'(',"ParCr":')',"LlavAp":'{',"LlavCr":'}',"CorAp":'[',"CorCr":']',"Igual":'=',"PtYcm":';',"DosPt":':',"Pt":'.',"Cma":',',"MenorQ":'<',"MayorQ":'>',"Mas":'+',"Guion":'-',"Div":'/',"Asterisco":'*',"Negacion":'!',"Barra":'|',"Appersan":'&',"Mod":'%'}

def obtenerRuta(texto):
    linea = str.split(texto,"\n")

    print(linea[0].__contains__("PATHL"))
    if linea[0].__contains__("PATHL"):        
        completa = linea[0].replace("//","")
        completa = completa.replace(" ","")
        print("si"+completa[6:])
        return completa[6:]
        
        

def AnalizadorJS(texto):
#En este metodo se pasa el texto para ver cual es la ER a la que pertenece y que parte del arbol se graficara
    global linea, columna, Errores, contador, tokens, textoLimpio, banderaSigno
    path = obtenerRuta(texto)
    linea = 0
    columna = 0
    listaToks = []
    

    while contador < len(texto):
       # print(contador)
        if re.search("[A-Za-z]",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Identificadores(linea,columna,texto,texto[contador]))
        elif re.search("[0-9]",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Numero(linea,columna,texto,texto[contador]))
        elif re.search("\"",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Cadena(linea,columna,texto,texto[contador]))
            columna += 1
            contador += 1
        elif re.search("[/]",texto[contador]):
            textoLimpio += texto[contador]
            NoSS =Comentario(linea,columna,texto,texto[contador])
            contador += 1
            columna += 1
        elif re.search("[ \t]", texto[contador]):
            textoLimpio += texto[contador]
            columna += 1
            contador += 1
        elif re.search("[\n]", texto[contador]):
            textoLimpio += texto[contador]
            columna = 0
            contador +=  1
            linea += 1
        elif re.search("'",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Character(linea, columna, texto, texto[contador]))
            contador += 1
            columna += 1
        else:
            validadorSigno = False

            for clave in simbolos:

                valor = simbolos[clave]
                #print(texto[contador])
                if re.search(r"["+valor+"]", texto[contador]):
    
                    listaToks.append([linea, columna, clave, valor.replace("//","")])
                    textoLimpio += texto[contador]
                    contador += 1
                    columna += 1
                    validadorSigno = True
                    banderaSigno = True
                    break
            
            if validadorSigno == False:
                columna += 1
                Errores.append([linea,columna,texto[contador]])
                contador += 1

    tokens = listaToks

    Reservadas()
    
    for token in tokens:
        print(token)

    for error in Errores:
        print(error)
    print(textoLimpio)
    archivoLimpio(path)
    expresionesUsadas(path)
    if Errores != None:
        archivoErrores(path)
    return tokens


def Identificadores(lineaa, columnaa, texto, palabra):

    global contador, columna, banderaID, textoLimpio
    contador += 1
    columna += 1
    
    if contador < len(texto):

        if re.search("[A-Za-z0-9_]",texto[contador]):
            textoLimpio += texto[contador]
            return Identificadores(lineaa,columnaa,texto, palabra + texto[contador])
        else:
            
            banderaID = True
            return [lineaa, columnaa, 'ID', palabra]
            #En este caso se aprueba la presecina de la expresion regular
    else:
        banderaID = True
        return [lineaa, columnaa, 'ID', palabra]


def Numero(lineaa, columnaa, texto, palabra):


    global contador, columna, banderaNum, validador, textoLimpio

    contador += 1
    columna += 1

    if contador < len(texto):

        if re.search("[0-9]",texto[contador]):
            textoLimpio += texto[contador]
            return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            
        elif re.search("[\.]",texto[contador]):
            if validador == True:
                textoLimpio += str(texto[contador])
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            else:
                validador = True
                textoLimpio += str(texto[contador])
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            banderaNum = True
            return [lineaa, columnaa, "Numero", palabra]        
            
            
    else:
        banderaNum = True
        return [lineaa, columnaa, "Numero", palabra]


def Cadena(lineaa, columnaa, texto, palabra):

    global linea, columna, contador, banderaCadena, textoLimpio

    columna+=1
    contador += 1

    if contador < len(texto):
        if re.search("[\n]", texto[contador]):
            linea += 1
            columna = 0
            textoLimpio += texto[contador]
            return Cadena(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("\"",texto[contador]):
            textoLimpio += texto[contador]
            banderaCadena = True
            return [lineaa, columnaa, "Cadena",palabra]
        else:
            textoLimpio += texto[contador]
            return Cadena(lineaa, columnaa, texto, palabra + texto[contador])
    else:
        textoLimpio += texto[contador]
        return [lineaa, columnaa, "Cadena",palabra]
        

def Comentario(lineaa, columnaa, texto, palabra):

    global columna, contador,textoLimpio

    columna += 1
    contador += 1

    if contador < len(texto):
        if re.search("[\*]",texto[contador]):
            textoLimpio += texto[contador]
            return ComentarioML(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("[/]",texto[contador]):
            textoLimpio += texto[contador]
            return ComentarioL(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            textoLimpio += texto[contador]
            return [lineaa,columnaa,"Comentario",palabra]
    else:
        textoLimpio += texto[contador]
        return [lineaa,columnaa,"Comentario",palabra]
    pass


def ComentarioL(lineaa, columnaa, texto, palabra):

    global linea,columna, contador, banderaComntL,textoLimpio

    columna += 1
    contador +=1

    if contador < len(texto):


        if re.search(r"[\n]", texto[contador]):
            textoLimpio += texto[contador]
            columna = 0
            linea += 1
            banderaComntL = True
            return [lineaa, columnaa, "", palabra]
        else:
            textoLimpio += texto[contador]
            return ComentarioL(lineaa, columnaa, texto, palabra + texto[columna])
    else:
        textoLimpio += texto[contador]
        banderaComntL = True
        return [lineaa, columnaa, "", palabra]


def ComentarioML(lineaa, columnaa, texto, palabra):
    global columna, linea, contador, banderaComntML, textoLimpio

    columna += 1
    contador +=1

    if contador < len(texto):

        if re.search("[\n]", texto[contador]):
            linea += 1
            columna = 0
            textoLimpio += texto[contador]
            return ComentarioML(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("[\*]", texto[contador]):
            textoLimpio += texto[contador]
            if (contador + 1) < len(texto):
                if texto[contador + 1] == "/":
                    contador+= 1
                    textoLimpio += texto[contador]
                    banderaComntML = True
                    return [lineaa, columnaa, "", palabra]
                else:
                    textoLimpio += texto[contador]
                    banderaComntML = True
                    return ComentarioML(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            textoLimpio += texto[contador]
            banderaComntML = True
            return ComentarioML(lineaa, columnaa, texto, palabra + texto[contador])
    else:
        banderaComntML = True
        textoLimpio += texto[contador]
        return [linea, columna, texto, palabra]

def Character(lineaa, columnaa, texto, palabra):
    global linea,columna, textoLimpio, contador, banderaChr
    columna += 1
    contador += 1

    if contador < len(texto):
        if re.search("[\n]", texto[contador]):
            linea += 1
            columna = 0
            textoLimpio += texto[contador]
            return Character(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("'",texto[contador]):
            banderaChr = True
            columna += 1
            textoLimpio += texto[contador]
            return [lineaa, columnaa, "Caracter",palabra]
        else:
            textoLimpio += texto[contador]
            return Character(lineaa, columnaa, texto, palabra + texto[contador])




def Reservadas():
    global tokens

    if tokens != None:
        for token in tokens:

            if "ID" in token:
                if token[3] == "console" or (token[3] == "if") or (token[3] == "var") or token[3] == "else" or token[3] == "for" or token[3] == "while" or token[3] == "do" or token[3] == "continue" or token[3] == "return" or token[3] == "function" or token[3] == "constructor" or token[3] == "class" or token[3] == "pow" or token[3] == "switch" or token[3] == "case" or token[3] == "new" or token[3] == "alert" or token[3] == "try" or token[3] == "catch" or token[3] == "in" or token[3] == "this" or token[3] == "log": 
                    token[2] = "Reservada"                                                                                                                                                                                                                                                                                              #"Math","pow","switch","case","new","alert","try","catch","in","this"
                elif (token[3] == "true") or (token[3] == "false"):
                    token[2] = "Booleano"
        
def expresionesUsadas(path):
    #L: Letras
    #D: Digitos
    #S: Slash
    #T: Todo
    #A: Asterisco
    #I: Salto de linea
    #C: Comilla
    #K: Simbolo
    #PU: Punto
    global banderaID, banderaComntML, banderaChr, banderaCadena, banderaComntL, banderaNum, banderaSigno

    expresionId = "..L*|L|D|__#"
    expresionNumerica = "..D.*D?.P.D*D#"
    expresionComentL = "..S.S*T_#"
    expresionComentML = "..S.A.*|TI.AS#"
    expresionCadena = "..C.*|TIC#"
    expresionSimbolo = ".K#"

    exrpGenral = ""

    expAux = ""    
    if banderaID:
        exrpGenral += "|"
        expAux += expresionId

    if banderaNum:
        exrpGenral += "|"
        expAux += expresionNumerica

    if banderaSigno:
        if banderaCadena == True:
            exrpGenral += "|"
            expAux += expresionCadena
        
        expAux += expresionSimbolo  
        exrpGenral += expAux

        


    '''
    if banderaComntML:
        c = Principal(expresionComentL, "Comentario_Linea")
    if banderaComntL:
        d = Principal(expresionComentML, "Comentario_MultiLinea")
    if banderaChr:
        e = Principal(expresionChar, "Cadena")
    if banderaCadena:
        f = Principal(expresionCadena, "Cadena")
    '''

    
    

    l = Principal(exrpGenral,path+"Reporte")


def archivoLimpio(path):
    global textoLimpio
    try:
        os.stat(path.strip())
    except:
        os.makedirs(path.strip())
    pass


    #file = open(path.strip()+"name.js","a")
    with open(path+"name.js","w+") as file:
        file.seek(0,0)
        file.write(textoLimpio)
        file.close()

def archivoErrores(path):
    global Errores

    with open(path+"Style.css","w+") as f:
        f.write("table {")
        f.write("table-layout: fixed;")
        f.write("width: 100%;")
        f.write("border-collapse: collapse;")
        f.write("}")
        f.close()

    with open(path+"ErroresJs.html","w+") as file:

        file.seek(0,0)

        file.write("<html>")
        file.write("<head>")
        file.write("<title>Errores JS</title>")
        file.write("<style type=\"text/css\">table{table-layout: fixed; width: 100%; border-collapse: collapse;}</style>")
        file.write("</head>")
        file.write("<body>")
        file.write("<h1>Tabla De Errores Lexicos</h1>")
        file.write("<table summary=\"Errores encontrados\">")
        file.write("<caption>Errores encontrados en el archivos de entrada</caption>")

        file.write("<thead>")


        file.write("<tr>")
        file.write("<th scope=\"col\">No.</th>")
        file.write("<th>Columna</th>")
        file.write("<th>File</th>")
        file.write("<th>Lexema</th>")
        file.write("</tr>")


        file.write("</thead>")


        file.write("<tbody>")
        file.write("</tbody>")
        cont = 1
        for error in Errores:
            file.write("<tr>")
            file.write("<th scope=\"row\">"+str(cont)+"</th>")
            file.write("<th scope=\"row\"> "+str(error[0])+"</th>")
            file.write("<th scope=\"row\">"+str(error[1])+"</th>")
            file.write("<th scope=\"row\">"+str(error[2])+"</th>")
            file.write("</tr>")

            cont += 1

        file.write("</table>")
        file.write("</body>")
        file.write("</html>")

        file.close()
    
    #os.system(path+"ErroresJs.html")
    webbrowser.open(path+"ErroresJs.html")
    pass




