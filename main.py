import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def on_closing_input():
    input_window.withdraw()
    check_exit()

def on_closing_visualizer():
    root.withdraw()
    check_exit()

def show_input_window():
    input_window.deiconify()

def show_visualizer_window():
    root.deiconify()

def check_exit():
    if root.state() == "withdrawn" and input_window.state() == "withdrawn":
        root.quit()

def close_app():
    if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
        root.destroy()
        input_window.destroy()

# Function to update the BINGO board
def actualizar_tablero(letra, numero):
    indice_letra = letras.index(letra)
    if 1 <= numero <= 15 and indice_letra == 0:
        indice = numero - 1
    elif 16 <= numero <= 30 and indice_letra == 1:
        indice = 15 + (numero - 16)
    elif 31 <= numero <= 45 and indice_letra == 2:
        indice = 30 + (numero - 31)
    elif 46 <= numero <= 60 and indice_letra == 3:
        indice = 45 + (numero - 46)
    elif 61 <= numero <= 75 and indice_letra == 4:
        indice = 60 + (numero - 61)
    else:
        messagebox.showerror("Error", "Balota no válida", parent=input_window)
        return
    marcar_numero(canvas_items[indice]['oval'], False)
    marcar_numero(control_canvas_items[indice]['rect'], False)

# Function to handle the entry of balls
def ingresar_balota():
    letra = entrada_letra.get().upper()
    try:
        numero = int(entrada_numero.get())
        if letra in letras:
            actualizar_tablero(letra, numero)
        else:
            messagebox.showerror("Error", "Balota no válida", parent=input_window)
    except ValueError:
        messagebox.showerror("Error", "Número no válido", parent=input_window)

# Function to mark and unmark numbers
def marcar_numero(item, confirm_unmark=True):
    color = canvas.itemcget(item, "fill")
    if color == "red":
        if confirm_unmark and messagebox.askyesno("Confirmar", "¿Está seguro de desmarcar el número?", parent=input_window):
            canvas.itemconfig(item, fill="white")
            control_canvas.itemconfig(item, fill="white")
    else:
        canvas.itemconfig(item, fill="red")
        control_canvas.itemconfig(item, fill="red")

# Function to unmark all balls
def desmarcar_todas():
    if messagebox.askyesno("Confirmar", "¿Está seguro de desmarcar todas las balotas?", parent=input_window):
        for item in canvas_items:
            canvas.itemconfig(item['oval'], fill="white")
        for item in control_canvas_items:
            control_canvas.itemconfig(item['rect'], fill="white")

# BINGO letters
letras = ['B', 'I', 'N', 'G', 'O']

# Configuration of the main window
root = tk.Tk()
root.title("BINGO - Visualización")
root.configure(bg="black")

# Create a menu for the main window
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Opciones", menu=file_menu)
file_menu.add_command(label="Mostrar ventana de entrada", command=show_input_window)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=close_app)

# Configure the grid of the main window to expand
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Size of the balls grid
cell_size = 40
grid_width = cell_size * 15
grid_height = cell_size * 5

# Increase the size of the logo by 25%
logo_width = int(grid_width * 1.25)
logo_height = int(grid_height * 1.25)

# Resize the logo to match the new size
logo_image = Image.open("logo.jpg")  # Replace "logo.png" with the path to your logo
logo_image = logo_image.resize((logo_width, logo_height), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)

# Add space for the logo at the top
frame_logo = tk.Frame(root, bg="black")
frame_logo.grid(row=0, column=0, sticky='nsew', pady=10)
label_logo = tk.Label(frame_logo, image=logo, bg="black")
label_logo.pack(expand=True, fill='both')

# Frame for the BINGO board in landscape
frame_tablero = tk.Frame(root, bg="black")
frame_tablero.grid(row=1, column=0, sticky='nsew', pady=10)

canvas = tk.Canvas(frame_tablero, bg="black", highlightthickness=0)
canvas.pack(expand=True, fill='both')

canvas_items = []
label_items = []

# Create the grid in horizontal format
for i, letra in enumerate(letras):
    y_offset = i * cell_size + 5
    label = canvas.create_text(30, y_offset + cell_size // 2, text=letra, font=("Arial", 36), fill="white", anchor="e")
    label_items.append(label)
    for j in range(15):
        x = j * cell_size + 60
        y = y_offset
        balota = canvas.create_oval(x, y, x + cell_size, y + cell_size, fill="white", outline="black")
        numero = canvas.create_text(x + cell_size // 2, y + cell_size // 2, text=str(j + 1 + i * 15), font=("Arial", 10), fill="black")
        canvas.tag_bind(balota, '<Button-1>', lambda event, b=balota: marcar_numero(b))
        canvas.tag_bind(numero, '<Button-1>', lambda event, b=balota: marcar_numero(b))
        canvas_items.append({'oval': balota, 'text': numero})

# Resize the Canvas when changing the window size
def resize_canvas(event):
    canvas_width = event.width - 50
    canvas_height = event.height
    for i, letra in enumerate(letras):
        y_offset = i * canvas_height / len(letras)
        canvas.coords(label_items[i], 30, y_offset + canvas_height / (2 * len(letras)))
        for j in range(15):
            index = i * 15 + j
            x = j * canvas_width / 15 + 60
            y = y_offset
            canvas.coords(canvas_items[index]['oval'], x, y, x + canvas_width / 15, y + canvas_height / len(letras))
            canvas.coords(canvas_items[index]['text'], x + canvas_width / 30, y + canvas_height / (2 * len(letras)))
            canvas.itemconfig(canvas_items[index]['text'], font=("Arial", int(canvas_width / 30)))

canvas.bind('<Configure>', resize_canvas)

# Secondary window for the entry of balls
input_window = tk.Toplevel(root)
input_window.title("BINGO - Entrada de Balotas")
input_window.configure(bg="black")

# Create a menu for the input window
menu_bar_input = tk.Menu(input_window)
input_window.config(menu=menu_bar_input)
file_menu_input = tk.Menu(menu_bar_input, tearoff=0)
menu_bar_input.add_cascade(label="Opciones", menu=file_menu_input)
file_menu_input.add_command(label="Mostrar visualizador", command=show_visualizer_window)
file_menu_input.add_separator()
file_menu_input.add_command(label="Salir", command=close_app)

frame_entrada = tk.Frame(input_window, bg="black")
frame_entrada.pack(pady=10)

tk.Label(frame_entrada, text="Letra:", bg="black", fg="white").grid(row=0, column=0)
entrada_letra = tk.Entry(frame_entrada, width=5)
entrada_letra.grid(row=0, column=1)

tk.Label(frame_entrada, text="Número:", bg="black", fg="white").grid(row=0, column=2)
entrada_numero = tk.Entry(frame_entrada, width=5)
entrada_numero.grid(row=0, column=3)

boton_ingresar = tk.Button(frame_entrada, text="Ingresar Balota", command=ingresar_balota, bg="black", fg="white")
boton_ingresar.grid(row=0, column=4, padx=10)

# Button to unmark all balls
boton_desmarcar_todas = tk.Button(frame_entrada, text="Desmarcar Todas", command=desmarcar_todas, bg="black", fg="white")
boton_desmarcar_todas.grid(row=1, column=0, columnspan=5, pady=10)

# Create control canvas for the input window
control_canvas = tk.Canvas(frame_entrada, bg="black", highlightthickness=0)
control_canvas.grid(row=2, column=0, columnspan=5, pady=10, sticky='nsew')

control_canvas_items = []
control_label_items = []

# Create the grid in horizontal format for the control canvas
control_cell_width = 40
control_cell_height = 20
for i, letra in enumerate(letras):
    y_offset = i * control_cell_height + 5
    label = control_canvas.create_text(20, y_offset + control_cell_height // 2, text=letra, font=("Arial", 18), fill="white", anchor="e")
    control_label_items.append(label)
    for j in range(15):
        x = j * control_cell_width + 40
        y = y_offset
        rect = control_canvas.create_rectangle(x, y, x + control_cell_width, y + control_cell_height, fill="white", outline="black")
        numero = control_canvas.create_text(x + control_cell_width // 2, y + control_cell_height // 2, text=str(j + 1 + i * 15), font=("Arial", 10), fill="black")
        control_canvas.tag_bind(rect, '<Button-1>', lambda event, b=rect: marcar_numero(b))
        control_canvas.tag_bind(numero, '<Button-1>', lambda event, b=rect: marcar_numero(b))
        control_canvas_items.append({'rect': rect, 'text': numero})

# Resize the control canvas when changing the window size
def resize_control_canvas(event):
    canvas_width = event.width - 50
    canvas_height = event.height
    for i, letra in enumerate(letras):
        y_offset = i * canvas_height / len(letras)
        control_canvas.coords(control_label_items[i], 20, y_offset + canvas_height / (2 * len(letras)))
        for j in range(15):
            index = i * 15 + j
            x = j * canvas_width / 15 + 40
            y = y_offset
            control_canvas.coords(control_canvas_items[index]['rect'], x, y, x + canvas_width / 15, y + canvas_height / len(letras))
            control_canvas.coords(control_canvas_items[index]['text'], x + canvas_width / 30, y + canvas_height / (2 * len(letras)))
            control_canvas.itemconfig(control_canvas_items[index]['text'], font=("Arial", int(canvas_width / 30)))

control_canvas.bind('<Configure>', resize_control_canvas)

input_window.grid_rowconfigure(2, weight=1)
input_window.grid_columnconfigure(0, weight=1)

# Bind the close event for both windows
root.protocol("WM_DELETE_WINDOW", on_closing_visualizer)
input_window.protocol("WM_DELETE_WINDOW", on_closing_input)

root.mainloop()
