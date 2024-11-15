import re
import os
import customtkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

# Expresiones regulares
PATRON_COMENTARIOS = re.compile(r'/\*\*([\s\S]*?)\*\*/')
PATRON_COMANDOS = re.compile(r'@(\w+)\s*(.*)')

def extraer_comentarios(file_path):
    """Lee el archivo C y extrae los comentarios de tipo /** .. **/."""
    with open(file_path, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
        comentarios = PATRON_COMENTARIOS.findall(contenido)
        return comentarios

def parser_comentarios(comentario):
    """Parsea comentarios y extrae los datos usando expresiones regulares"""
    dato = {'name': [], 'params': [], 'return': '', 'error': '', 'extra': ''}

    for match in PATRON_COMANDOS.finditer(comentario):
        comando, descripcion = match.groups()
        if comando == 'name':
            name_name, name_desc = descripcion.split(' ', 1)
            dato['name'].append((name_name, name_desc))
        elif comando == 'param':
            param_name, param_desc = descripcion.split(' ', 1)
            dato['params'].append((param_name, param_desc))
        elif comando == 'return':
            dato['return'] = descripcion
        elif comando == 'error':
            dato['error'] = descripcion
        elif comando == 'extra':
            dato['extra'] = descripcion
    return dato

def generar_html(comentarios, output_file):
    """Genera el archivo HTML a partir de los comentarios procesados."""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Documentación de funciones</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <div class="container">
            <header>Documentación Generada</header>
    """

    for comentario in comentarios:
        dato = parser_comentarios(comentario)
        html += """
            <br>
            <div class="function-block">
                <table class="function-table">"""
        for name_name, name_desc in dato['name']:
            html += f"""
                <tr>
                    <th>Nombre</th>
                    <td><b>{name_name}</b><br> {name_desc}</td>
                </tr>"""
        if dato['params']:
            for param_name, param_desc in dato['params']:
                html += f"""
                    <tr>
                        <th>Parámetro</th>
                        <td><b>{param_name}</b><br> {param_desc}</td>
                    </tr>"""
        html += f"""
            <tr>
                <th>Retorna</th>
                <td>{dato['return']}</td>
            </tr>"""
        if dato['error']:
            html += f"""
                <tr>
                    <th>Error</th>
                    <td>{dato['error']}</td>
                </tr>"""
        if dato['extra']:
            html += f"""
                <tr>
                    <th>Doc. Adicional</th>
                    <td>{dato['extra']}</td>
                </tr>"""
        html += """
            </table>
        </div>
        """
    html += """
            <a href="#" class="volver-inicio">Inicio</a>
        </div>
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as archivo:
        archivo.write(html)

def abrir_documentacion(output_file):
    """Abre el archivo HTML generado en el navegador predeterminado."""
    webbrowser.open(output_file)

def abrir_file_dialog():
    """Abre un cuadro de diálogo para seleccionar el archivo C y procesarlo."""
    file_path = filedialog.askopenfilename(
        initialdir=os.path.dirname(os.path.abspath(__file__)),
        filetypes=[("Archivos C", "*.c")])
    if file_path:
        output_file = file_path.rsplit('.', 1)[0] + "_documentacion.html"
        try:
            comentarios = extraer_comentarios(file_path)
            generar_html(comentarios, output_file)
            messagebox.showinfo("Éxito", f"Documentación generada con éxito: {output_file}")
            # Muestra el botón para abrir el archivo HTML
            btn_abrir_web.configure(command=lambda: abrir_documentacion(output_file))
            btn_abrir_web.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al procesar el archivo: {e}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo")

def crear_ui():
    """Crea la interfaz con CustomTkinter."""
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("dark-blue")
    
    root = tk.CTk()
    root.title("CDOC")
    
    # Dimensiones de la ventana
    window_width = 500
    window_height = 250
    
    # Obtiene el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcula la posición para centrar la ventana
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2) + 200

    # Establece la geometría de la ventana con un pequeño ajuste adicional
    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
    
    # Evitar que la ventana se redimensione
    root.resizable(False, False)

    # Crear un marco para los widgets principales
    frame_principal = tk.CTkFrame(root)
    frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

    # Etiqueta principal
    label = tk.CTkLabel(frame_principal, text="Generador de Documentación para Archivos C", font=("Arial", 14, "bold"))
    label.pack(pady=(10, 20))

    # Botón para seleccionar archivo
    btn_abrir_archivo = tk.CTkButton(frame_principal, text="Seleccionar archivo", command=abrir_file_dialog, width=20, font=('Arial', 12))
    btn_abrir_archivo.pack(pady=10)

    # Botón para abrir el archivo HTML
    global btn_abrir_web
    btn_abrir_web = tk.CTkButton(frame_principal, text="Visitar Página web", width=20, font=('Arial', 12))

    root.mainloop()

if __name__ == "__main__":
    crear_ui()