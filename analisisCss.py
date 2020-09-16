import re
import webbrowser
import os

contador = 0
columna = 0
fila = 0


reservadas = ["color","border","text-aling","front-wigth","padding-left","padding-top","line-height","margin-top","margin-left","display","top","float","min-width","background-color","Opacity","font-family","font-zise","padding-right","padding","width","margin-right","margin","position","right","clear","max-height","background-image","background","font-style","font","padding-bottom","display","height","margin-bottom","border-style","bottom","left","max-widht","min-height"]


simbolos = {"ParAp":'(',"ParCr":')',"LlavAp":'{',"LlavCr":'}',"CorAp":'[',"CorCr":']',"Igual":'=',"PtYcm":';',"DosPt":':',"Pt":'.',"Cma":',',"MenorQ":'<',"MayorQ":'>',"Mas":'+',"Guion":'-',"Div":'/',"Mod":'%'}


tokens = []
Errores = []
textoLimpioCss = ""

validador = False

reporte = []

def obtenerRuta(texto):
    linea = str.split(texto,"\n")

    print(linea[0].__contains__("PATHL"))
    if linea[0].__contains__("PATHL"):        
        completa = linea[0].replace("//","")
        completa = completa.replace(" ","")
        print("si"+completa[6:])
        return completa[6:]
        
        

def AnalizadorCss(text):
    global contador, columna, fila, tokens, Errores, textoLimpioCss, reporte

    listaToks = []

    while contador < len(text):

        if re.search("[A-Za-z]",text[contador]):
            textoLimpioCss += text[contador]
            reporte.append([fila, columna, text[contador], "Estado 1","Aceptado"])
            listaToks.append(Identificador(fila, columna, text, text[contador]))
            pass
        elif re.search(r"[\.]",text[contador]):
            textoLimpioCss += text[contador]
            reporte.append([fila, columna, text[contador],"Estado 1","Aceptado"])
            listaToks.append(Clase(fila, columna, text, text[contador]))
            pass
        elif re.search("[#]",text[contador]):
            textoLimpioCss += text[contador]
            reporte.append([fila, columna, text[contador],"Estado 1","Aceptado"])
            listaToks.append(Identificador(fila, columna, text, text[contador]))
        elif re.search("[0-9]",text[contador]):
            textoLimpioCss += text[contador]
            reporte.append([fila, columna, text[contador],"Estado 2","Aceptado"])
            listaToks.append(Numero(fila, columna, text, text[contador]))
            pass
        elif re.search("\"",text[contador]):
            textoLimpioCss += text[contador]
            reporte.append([fila, columna, text[contador],"Estado 10","Aceptado"])
            listaToks.append(Cadena(fila,columna,text,text[contador]))
            columna += 1
            contador += 1
            pass
        elif re.search("[ \t]",text[contador]):
            textoLimpioCss += text[contador]
            columna += 1
            contador += 1
            pass
        elif re.search("[\n]",text[contador]):
            textoLimpioCss += text[contador]
            columna = 0
            fila += 1
            contador += 1
            pass
        elif re.search("[/]",text[contador]):
            textoLimpioCss += text[contador]
            reporte.append([fila, columna, text[contador],"Estado 5","Aceptado"])
            NoSS =Comentario(fila,columna,text,text[contador])
            #print(NoSS)
            contador += 1
            columna += 1            
            pass
        
        else:
            validadorSigno = False

            for clave in simbolos:
                valor = simbolos[clave]
                
                if re.search(r"["+valor+"]",text[contador]):
                    listaToks.append([fila,columna,clave,valor.replace("//","")])
                    textoLimpioCss += text[contador]
                    reporte.append([fila, columna, text[contador],"Estado 9","Aceptado"])
                    contador += 1
                    columna += 1
                    validadorSigno = True
                    break
            
            if validadorSigno == False:
                columna += 1
                reporte.append([fila, columna, text[contador],"Estado X","ERROR"])
                Errores.append([fila, columna,text[contador]])
                contador += 1
    
    tokens = listaToks
    Reservadas()
    Reporte()
    path = obtenerRuta(text)
    archivoLimpio(path.strip())
    ReporteErrores(path.strip())
    print(textoLimpioCss)
    return tokens
    

def Identificador(lineaa, columnaa, texto, palabra):
    global contador, columna, textoLimpioCss, reporte

    contador += 1
    columna += 1

    if contador < len(texto):

        if re.search("[A-Za-z0-9_-]",texto[contador]):
            textoLimpioCss += texto[contador]
            reporte.append([fila, columna, texto[contador],"Estado 1","Aceptado"])
            return Identificador(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            return [lineaa, columnaa, "ID",palabra]
    else:
        return [lineaa, columnaa, "ID", palabra]

def Numero(lineaa, columnaa, texto, palabra):
    global contador, columna, textoLimpioCss, validador, reporte

    contador += 1
    columna += 1

    if contador < len(texto):
        if re.search("[0-9]",texto[contador]):
            textoLimpioCss += texto[contador]
            return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            
        elif re.search("[\.]",texto[contador]):
            if validador == True:
                textoLimpioCss += str(texto[contador])
                reporte.append([fila, columna, texto[contador],"Estado 3","Esperando estado 4"])
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
            else:
                validador = True
                textoLimpioCss += str(texto[contador])
                reporte.append([fila, columna, texto[contador],"Estado 4","Aceptado"])
                return Numero(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            return [lineaa, columnaa, "Numero", palabra]        
            
            
    else:
        return [lineaa, columnaa, "Numero", palabra]
    pass

def Cadena(lineaa, columnaa, texto, palabra):
    global fila, columna, contador, textoLimpioCss, reporte

    if contador < len(texto):
        if re.search("[\n]", texto[contador]):
            fila += 1
            columna = 0
            reporte.append([fila, columna, texto[contador],"Estado 10","Aceptado"])
            textoLimpioCss += texto[contador]
            return Cadena(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("\"",texto[contador]):
            textoLimpioCss += texto[contador]
            
            return [lineaa, columnaa, "Cadena",palabra]
        else:
            textoLimpioCss += texto[contador]
            reporte.append([fila, columna, texto[contador],"Estado 10","Aceptado"])
            return Cadena(lineaa, columnaa, texto, palabra + texto[contador])
    else:
        textoLimpioCss += texto[contador]
        return [lineaa, columnaa, "Cadena",palabra]

def Comentario(lineaa, columnaa, texto, palabra):
    global fila, columna, contador, textoLimpioCss
    columna += 1
    contador += 1

    if contador < len(texto):
        if re.search("[\*]",texto[contador]):
            textoLimpioCss += texto[contador]
            reporte.append([fila, columna, texto[contador],"Estado 6","Aceptado"])
            return Comentario2(lineaa, columnaa, texto, palabra)
        else:
            textoLimpioCss += texto[contador]
            return [lineaa, columnaa, "Comentario", palabra]
    else:
        return [lineaa, columnaa, "Comentario", palabra]

def Comentario2(lineaa, columnaa, texto, palabra):
    global fila, columna, contador, textoLimpioCss

    columna += 1
    contador +=1

    if contador < len(texto):

        if re.search("[\n]", texto[contador]):
            fila += 1
            columna = 0
            textoLimpioCss += texto[contador]
            return Comentario2(lineaa, columnaa, texto, palabra + texto[contador])
        elif re.search("[\*]", texto[contador]):
            textoLimpioCss += texto[contador]
            reporte.append([fila, columna, texto[contador],"Estado 7","Aceptado"])
            if (contador + 1) < len(texto):
                if texto[contador + 1] == "/":
                    contador+= 1
                    textoLimpioCss += texto[contador]
                    reporte.append([fila, columna, texto[contador],"Estado 8","Aceptado"])
                    return [lineaa, columnaa, "", palabra]
                else:
                    textoLimpioCss += texto[contador]

                    return Comentario2(lineaa, columnaa, texto, palabra + texto[contador])
        else:
            textoLimpioCss += texto[contador]
            reporte.append([fila, columna, texto[contador],"Estado 6","Aceptado"])
            return Comentario2(lineaa, columnaa, texto, palabra + texto[contador])
    else:
   
        return [lineaa, columnaa, texto, palabra]

def Clase(lineaa, columnaa, texto, palabra):
    global fila, columna, contador,textoLimpioCss, reporte

    columna += 1
    contador += 1

    if contador < len(texto):

        if re.search(r"[A-Za-z0-9_\-]",texto[contador]):
            textoLimpioCss += texto[contador]
            reporte.append([fila, columna, texto[contador],"Estado 1","Aceptado"])
            return Clase(lineaa,columnaa,texto,palabra + texto[contador])
        else:
            return [lineaa, columnaa, 'ID', palabra]
    
    else:
        return [lineaa, columnaa, 'ID', palabra]


def Reservadas():
    global tokens, reservadas

    for token in tokens:

        if 'ID' in token:
            tipo = str(token[3]) 

            if tipo in reservadas:
                token[2] = "Reservada"

    pass


def Reporte():
    global reporte

    string = ""

    for estado in reporte:
        
        string += str(estado) + "\n"

    return string


def archivoLimpio(path):
    global textoLimpioCss
    try:
        os.stat(path.strip())
    except:
        os.makedirs(path.strip())
    pass


    #file = open(path.strip()+"name.js","a")
    with open(path+"name.css","w+") as file:
        file.seek(0,0)
        file.write(textoLimpioCss)
        file.close()


def ReporteErrores(path):
    global Errores
    print(path)
    with open(path+"ErroresCss.html","w+") as file:

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

    webbrowser.open(path+"ErroresCss.html")