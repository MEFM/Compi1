from tkinter import Tk, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog, Text

import analisis

root = Tk()
root.title("Proyecto 1. MEFM.")
root.configure(background = "Gray")

'''FUNCIONES DEL MENU'''

archivo = ""

def nuevo():
    global archivo
    editor.delete(1.0, END)#ELIMINAR EL CONTENIDO
    archivo = ""

def abrir():
    global archivo
    archivo = filedialog.askopenfilename(title = "Abrir Archivo", initialdir = "C:/")

    entrada = open(archivo)
    content = entrada.read()

    editor.delete(1.0, END)
    editor.insert(INSERT, content)
    entrada.close()

def salir():
    value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
    if value :
        root.destroy()

def acercaDe():
    value = messagebox.askokcancel("Mynor Estuardo Florian Machado","MEFM, 201700371.\nProyecto1 Compiladores 1.")
    if value:
        pass

def guardarArchivo():
    global archivo
    if archivo == "":
        guardarComo()
    else:
        guardarc = open(archivo, "w")
        guardarc.write(editor.get(1.0, END))
        guardarc.close()

def guardarComo():
    global archivo
    guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/")
    fguardar = open(guardar, "w+")
    fguardar.write(editor.get(1.0, END))
    fguardar.close()
    archivo = guardar

def reportes():

    pass

def analizarTexto():
    texto = editor.get(1.0,END)

    editor.tag_config("Reservada",foreground ="red")
    editor.tag_config("Identificador",foreground ="green")
    editor.tag_config("Cadea",foreground ="yelow")
    editor.tag_config("BoolNum",foreground ="blue")
    editor.tag_config("Operadores",foreground ="orange")
    editor.tag_config("Otro",foreground ="black")

    tokens = analisis.AnalizadorJS(texto)

    

            



    

    




barraMenu = Menu(root)
root.config(menu = barraMenu, width = 1000, height = 600)

archivoMenu = Menu(barraMenu, tearoff=0)
archivoMenu.add_command(label = "Nuevo", command = nuevo)
archivoMenu.add_command(label = "Abrir", command = abrir)
archivoMenu.add_command(label = "Guardar", command = guardarArchivo)
archivoMenu.add_command(label = "Guardar Como...", command = guardarComo)

analisisMenu = Menu(barraMenu, tearoff = 0)
analisisMenu.add_command(label = "Analizar archivo", command = analizarTexto)
analisisMenu.add_command(label = "Reportes", command = reportes())

barraMenu.add_cascade(label = "Archivo", menu = archivoMenu)
barraMenu.add_cascade(label = "Analisis", menu = analisisMenu)
barraMenu.add_command(label = "Acerca de...",  command = acercaDe)
barraMenu.add_command(label = "Salir",  command = salir)


frame = Frame(root, bg="Gray")
canvas = Canvas(frame, bg="Gray")
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scroll = Frame(canvas, bg="Gray")

scroll.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set, width = 920, height = 750)

editor = scrolledtext.ScrolledText(scroll, undo = True, width = 60, height = 15, font = ("Arial", 15), background = 'White',  foreground = "Black")

editor.grid(column = 1, row = 1, pady = 25, padx = 125)


terminalEditor = scrolledtext.ScrolledText( undo = True, width = 60, height = 10, font = ("Arial",15),background = 'Black', foreground = "Green")
terminalEditor.grid(column = 1, row = 1, pady = 5, padx = 150)
terminalEditor.place(x = 125,y = 450)


frame.grid(sticky='news')
canvas.grid(row=0,column=1)
scrollbar.grid(row=0, column=2, sticky='ns')



editor.focus()
terminalEditor.focus()
root.mainloop()