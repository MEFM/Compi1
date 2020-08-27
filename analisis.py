import re

#Banderas de expresiones

banderaID = False
banderaNum = False
banderaComntL = False
banderaComntML = False
banderaCadena = False
banderaSigno = False

#Bandera Especial para numeros 
validador = False


#Contadores de texto
linea = 0
columna = 0
contador = 0

textoLimpio = ""

Errores = []
tokens = []

palabrasReservadas = ["var","if","for","while","do","Continue","break","else","return","function","constructor","class","Math","pow","switch","case"]
simbolos = {"ParAp":'(',"ParCr":')',"LlavAp":'{',"LlavCr":'}',"CorAp":'[',"CorCr":']',"Igual":'=',"PtYcm":';',"DosPt":':',"Pt":'.',"Cma":',',"MenorQ":'<',"MayorQ":'>',"Mas":'+',"Guion":'-',"Div":'/',"Asterisco":'*',"Negacion":'!',"Barra":'|',"Appersan":'&',"Mod":'%'}

def AnalizadorJS(texto):
#En este metodo se pasa el texto para ver cual es la ER a la que pertenece y que parte del arbol se graficara
    global linea, columna, Errores, contador, tokens, textoLimpio

    linea = 0
    columna = 0
    listaToks = []

    while contador < len(texto):
        print(contador)
        if re.search("[A-Za-z]",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Identificadores(linea,columna,texto,texto[contador]))
        elif re.search("[0-9]",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Numero(linea,columna,texto,texto[contador]))
        elif re.search("\"",texto[contador]):
            textoLimpio += texto[contador]
            listaToks.append(Cadena(linea,columna,texto,texto[contador]))
        elif re.search("[/]",texto[contador]):
            textoLimpio += texto[contador]
            NoSS =Comentario(linea,columna,texto,texto[contador])
        elif re.search("[ \t]", texto[contador]):
            textoLimpio += texto[contador]
            columna += 1
            contador += 1
        elif re.search("[\n]", texto[contador]):
            textoLimpio += texto[contador]
            columna = 0
            contador +=  1
            linea += 1
        else:
            validadorSigno = False

            for clave in simbolos:

                valor = simbolos[clave]
                print(texto[contador])
                if re.search(r"["+valor+"]", texto[contador]):
    
                    listaToks.append([linea, columna, clave, valor.replace("//","")])
                    textoLimpio += texto[contador]
                    contador += 1
                    columna += 1
                    validadorSigno = True
                    break
            
            if validadorSigno == False:
                columna += 1
                Errores.append([linea,columna,texto[contador]])
                contador += 1

    tokens = listaToks
    print(tokens)

    print(textoLimpio)
    Reservadas()
    
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
        
        if re.search("[.]",texto[contador]):
            textoLimpio += texto[contador]
            return Cadena(lineaa, columnaa,  texto, palabra + texto[contador])
        elif re.search("[\n]",texto[contador]):
            linea +=1
            columna = 0
            textoLimpio += texto[contador]
            return Cadena(lineaa, columnaa,  texto, palabra + texto[contador])
        elif re.search("[\"]",texto[contador]):
            banderaCadena = True
            textoLimpio += texto[contador]
            return [lineaa, columnaa, "Cadena", palabra]
        


    else:
        banderaCadena = True
        return [lineaa, columnaa, "Cadena", palabra]
        

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
            return [lineaa,columnaa,"",palabra]
    else:
        textoLimpio += texto[contador]
        return [lineaa,columnaa,"",palabra]
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
            return ComentarioML(linea, columna, texto, palabra + texto[contador])
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
                    return ComentarioML(linea, columna, texto, palabra + texto[contador])
        else:
            textoLimpio += texto[contador]
            return ComentarioML(linea, columna, texto, palabra + texto[contador])
    else:
        banderaComntML = True
        textoLimpio += texto[contador]
        return [linea, columna, texto, palabra]


def Reservadas():
    global tokens

    for token in tokens:

        if "ID" in token:
            if (token[3] == "if") or (token[3] == "var") or token[3] == "else" or token[3] == "for" or token[3] == "while" or token[3] == "do" or token[3] == "continue" or token[3] == "return" or token[3] == "function" or token[3] == "constructor" or token[3] == "class": 
                token[2] = "Reservada"
               


