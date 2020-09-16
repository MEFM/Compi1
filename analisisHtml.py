import re
import os
import webbrowser

contador = 0
columna = 0
fila = 0

textoLimpioHtml = ""

reservadas = ["html","head","title","body","h1","h2","h3","h4","h5","h6","p","img","a","ol","ul","il","style","table","th","tr","td","caption","colgroup","col","thead","tbody","tbody"]

simbolos = {"Igual":'=',"DosPt":':',"PtYcm":';',"Pt":'.',"Cma":',',"Mas":'+',"Guion":'-', "Slash": '/'}

tokens = []
Errores = []

validador = False



def obtenerRuta(texto):

    linea = str.split(texto,"\n")

    print(linea[0].__contains__("PATHL"))
    if linea[0].__contains__("PATHL"):        
        completa = linea[0].replace("//","")
        completa = completa.replace(" ","")
        print("si"+completa[6:])
        return completa[6:]


def AnalizadorHtml(texto):
    global contador, columna, fila, tokens, Errores, textoLimpioHtml, simbolos
    path = obtenerRuta(texto)
    listaTokens = []
    lineaPTH = str.split(texto, "\n")

    tamanioPATH = len(lineaPTH[0])

    contador = tamanioPATH
    bandera = False

    while contador < len(texto):

        if contador < len(texto):

            
            if bandera == False:
                textoLimpioHtml += texto[contador]
                
                if re.search("[ \t]", texto[contador]):
                    columna += 1
                    contador += 1
                elif re.search("[\n]", texto[contador]):
                    columna = 0
                    contador +=  1
                    columna += 1
                else:
                    if re.search(r"[\<]",texto[contador]):
                        bandera = True
                    columna += 1
                    contador += 1

            else:
                if re.search(r"[\<]",texto[contador]):
                    
                    textoLimpioHtml += texto[contador]
                    listaTokens.append([fila,columna,"MenorQ",texto[contador+1]])
                    contador += 1
                    columna += 1
                    bandera = True
                elif re.search(r"[\>]", texto[contador]):
                    textoLimpioHtml += texto[contador]
                    listaTokens.append([fila,columna,"MenorQ",texto[contador+1]])
                    bandera = False
                    contador += 1
                    columna +=1
                elif re.search("[A-Za-z]",texto[contador]):
                    if bandera == False:
                        textoLimpioHtml += texto[contador]
                        
                    else:
                        textoLimpioHtml += texto[contador]
                        listaTokens.append(Identificador(fila, columna, texto, texto[contador]))
                elif re.search("\"",texto[contador]):
                    if bandera == False:
                        textoLimpioHtml += texto[contador]
                    else:
                        textoLimpioHtml += texto[contador]
                        listaTokens.append(Cadena(fila,columna,texto,texto[contador]))
                        contador += 1
                        columna += 1

                elif re.search("[0-9]", texto[contador]):
                    if bandera == False:
                        textoLimpioHtml += texto[contador]
                    else:
                        textoLimpioHtml += texto[contador]
                        listaTokens.append(Numero(fila, columna, texto, texto[contador]))        
                elif re.search("'",texto[contador]):
                    if bandera == False:
                        textoLimpioHtml += texto[contador]
                    else:
                        textoLimpioHtml += texto[contador]
                        listaTokens.append(Cadenachr(fila,columna,texto,texto[contador]))
                        contador += 1
                        columna += 1

                elif re.search("[ \t]", texto[contador]):
                    textoLimpioHtml += texto[contador]
                    columna += 1
                    contador += 1
                elif re.search("[\n]", texto[contador]):
                    textoLimpioHtml += texto[contador]
                    columna = 0
                    contador +=  1
                    columna += 1

                else:
                
                    if bandera == False:
                        textoLimpioHtml += texto[contador]
                    else:
                        validadorSigno = False

                        for clave in simbolos:
                            valor = simbolos[clave]

                            if re.search(r"["+valor+"]",texto[contador]):
                                listaTokens.append([fila,columna,clave,valor.replace("//","")])
                                textoLimpioHtml += texto[contador]
                                contador += 1
                                columna += 1
                                validadorSigno = True
                                break

                        if validadorSigno == False:
                            columna += 1
                            Errores.append([fila, columna, texto[contador]])
                            contador += 1
                
            pass



    archivoLimpio(path)
    ReporteErrores(path)
    print(textoLimpioHtml)
    tokens = listaTokens
    Reservadas()

    for token in tokens:
        print(token)
    return listaTokens


def ComentInit(lineaa, columnaa, texto, palabra):

    global columna, contador,textoLimpioHtml

    columna += 1
    contador += 1

    if contador < len(texto):
        if re.search("[/]",texto[contador]):
            textoLimpioHtml += texto[contador]
            return ComentarioL(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            textoLimpioHtml += texto[contador]
            return [lineaa,columnaa,"Comentario",palabra]
    else:
        textoLimpioHtml += texto[contador]
        return [lineaa,columnaa,"Comentario",palabra]
    pass    

def ComentarioL(lineaa, columnaa, texto, palabra):
    
    global fila,columna, contador,textoLimpioHtml

    columna += 1
    contador +=1

    if contador < len(texto):


        if re.search(r"[\n]", texto[contador]):
            textoLimpioHtml += texto[contador]
            columna = 0
            fila += 1
            return [lineaa, columnaa, "", palabra]
        else:
            textoLimpioHtml += texto[contador]
            return ComentarioL(lineaa, columnaa, texto, palabra + texto[columna])
    else:
        textoLimpioHtml += texto[contador]
        return [lineaa, columnaa, "", palabra]


def Identificador(lineaa, columnaa, texto, palabra):
    global contador, columna, textoLimpioHtml

    contador += 1
    columna += 1

    if contador < len(texto):

        if re.search("[A-Za-z0-9_]",texto[contador]):
            textoLimpioHtml += texto[contador]
            return Identificador(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            return [lineaa, columnaa, "ID",palabra]
    else:
        return [lineaa, columnaa, "ID", palabra]

    pass

def Numero(lineaa, columnaa, texto, palabra):
    global contador, columna, textoLimpioHtml, validador

    contador += 1
    columna += 1

    if contador < len(texto):
        if re.search("[0-9]",texto[contador]):
            textoLimpioHtml += texto[contador]
            return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            
        elif re.search(r"[\.]",texto[contador]):
            if validador == True:
                textoLimpioHtml += str(texto[contador])
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            else:
                validador = True
                textoLimpioHtml += str(texto[contador])
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            return [lineaa, columnaa, "Numero", palabra]        
            
            
    else:
        return [lineaa, columnaa, "Numero", palabra]
    pass

def Cadena(lineaa, columnaa, texto, palabra):
    global fila, columna, contador, textoLimpioHtml

    if contador < len(texto):
        if re.search("[\n]", texto[contador]):
            fila += 1
            columna = 0
            textoLimpioHtml += texto[contador]
            return Cadena(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("\"",texto[contador]):
            textoLimpioHtml += texto[contador]            
            return [lineaa, columnaa, "Cadena",palabra]
        else:
            textoLimpioHtml += texto[contador]
            return Cadena(lineaa, columnaa, texto, palabra + texto[contador])
    else:
        textoLimpioHtml += texto[contador]
        return [lineaa, columnaa, "Cadena",palabra]    

def Cadenachr(lineaa, columnaa, texto, palabra):
    global fila, columna, contador, textoLimpioHtml, reporte

    if contador < len(texto):
        if re.search("[\n]", texto[contador]):
            fila += 1
            columna = 0
            textoLimpioHtml += texto[contador]
            return Cadenachr(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("'",texto[contador]):
            textoLimpioHtml += texto[contador]            
            return [lineaa, columnaa, "Cadena",palabra]
        else:
            textoLimpioHtml += texto[contador]
            return Cadenachr(lineaa, columnaa, texto, palabra + texto[contador])
    else:
        textoLimpioHtml += texto[contador]
        return [lineaa, columnaa, "Cadena",palabra]        

def archivoLimpio(path):
    global textoLimpioHtml
    try:
        os.stat(path.strip())
    except:
        os.makedirs(path.strip())
    
    
    with open(path+"name.html","w+") as file:
        file.seek(0,0)
        file.write(textoLimpioHtml.replace("\"\"","\""))
        file.close()

def ReporteErrores(path):
    global Errores
    print(path)
    with open(path+"ErroresHtml.html","w+") as file:

        file.seek(0,0)

        file.write("<html>")
        file.write("<head>")
        file.write("<title>Errores Css</title>")
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

    webbrowser.open(path+"ErroresHtml.html")

def Reservadas():
    global reservadas, tokens

    for token in tokens:

        if 'ID' in token:
            tipo = str(token[3])

            if tipo in reservadas:
                token[2] = "Reservada"

