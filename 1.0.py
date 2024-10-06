import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import re

# Función para validar si una fecha es válida usando una expresión regular
def es_fecha_valida(fecha):
    return re.match(r'\d{4}-\d{2}-\d{2}', fecha) is not None

# Función para validar la entrada del usuario antes de agregar o actualizar un centro de cultivo
def validar_entrada():
    if not entrada_id.get().isdigit():
        messagebox.showerror("Error", "El ID debe ser un número.")
        return False
    if not entrada_nombre_centro.get().strip():
        messagebox.showerror("Error", "El Nombre del Centro de Cultivo no puede estar vacío.")
        return False
    if entrada_fecha_entrega.get() and not es_fecha_valida(entrada_fecha_entrega.get()):
        messagebox.showerror("Error", "Fecha de entrega no es válida. Debe estar en formato AAAA-MM-DD.")
        return False
    if entrada_fecha_desinstalacion.get() and not es_fecha_valida(entrada_fecha_desinstalacion.get()):
        messagebox.showerror("Error", "Fecha de desinstalación no es válida. Debe estar en formato AAAA-MM-DD.")
        return False
    return True

# Función para conectar a la base de datos MySQL
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="checc1987",
            database="gestion_centros_cultivo"
        )
        return conexion
    except Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

# Función para agregar un nuevo centro de cultivo a la base de datos
def agregar_centro():
    if validar_entrada():
        conexion = conectar_bd()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = """
                INSERT INTO Centros_Cultivo (ID, NombreCentro, NombrePonton, FechaEntrega, FechaDesinstalacion, 
                NumeroModulo, JaulasPorModulo, MedidasJaula, TipoSistemaVideo, TipoSistemaAlimentacion, 
                NombreEjecutantesInstalacion, NombreEjecutantesDesinstalacion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    entrada_id.get(), entrada_nombre_centro.get(), entrada_nombre_ponton.get(),
                    entrada_fecha_entrega.get() or None, entrada_fecha_desinstalacion.get() or None,
                    entrada_numero_modulo.get(), entrada_jaulas_modulo.get(), entrada_medidas_jaula.get(),
                    entrada_tipo_video.get(), entrada_tipo_alimentacion.get(),
                    entrada_nombre_ejecutantes_instalacion.get(), entrada_nombre_ejecutantes_desinstalacion.get()
                )
                cursor.execute(sql, valores)
                conexion.commit()
                messagebox.showinfo("Información", "Añadido exitosamente")
                mostrar_lista()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo agregar el centro de cultivo: {e}")
            finally:
                conexion.close()

# Función para mostrar la lista de centros de cultivo en la interfaz
def mostrar_lista():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Centros_Cultivo")
            filas = cursor.fetchall()
            lista.delete(0, tk.END)
            for fila in filas:
                lista.insert(tk.END, fila)
        except Error as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista: {e}")
        finally:
            conexion.close()

# Función para eliminar un centro de cultivo seleccionado de la base de datos
def eliminar_centro():
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            selected_item = lista.curselection()
            if selected_item:
                item = lista.get(selected_item)
                cursor.execute("DELETE FROM Centros_Cultivo WHERE ID = %s", (item[0],))
                conexion.commit()
                messagebox.showinfo("Información", "Eliminado exitosamente")
                mostrar_lista()
            else:
                messagebox.showwarning("¡Advertencia!", "Selecciona un centro de cultivo para eliminar")
        except Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar el centro de cultivo: {e}")
        finally:
            conexion.close()

# Función para actualizar un centro de cultivo existente en la base de datos
def actualizar_centro():
    selected_item = lista.curselection()
    if not selected_item:
        messagebox.showwarning("¡Advertencia!", "Selecciona un centro de cultivo para actualizar.")
        return
    item = lista.get(selected_item)
    id_centro = item[0]
    nuevo_nombre_centro = entrada_nombre_centro.get().strip() or None
    nuevo_nombre_ponton = entrada_nombre_ponton.get().strip() or None
    nueva_fecha_entrega = entrada_fecha_entrega.get().strip() or None
    nueva_fecha_desinstalacion = entrada_fecha_desinstalacion.get().strip() or None
    nuevo_numero_modulo = entrada_numero_modulo.get().strip() or None
    nuevas_jaulas_modulo = entrada_jaulas_modulo.get().strip() or None
    nuevas_medidas_jaula = entrada_medidas_jaula.get().strip() or None
    nuevo_tipo_video = entrada_tipo_video.get().strip() or None
    nuevo_tipo_alimentacion = entrada_tipo_alimentacion.get().strip() or None
    nuevo_nombre_ejecutantes_instalacion = entrada_nombre_ejecutantes_instalacion.get().strip() or None
    nuevo_nombre_ejecutantes_desinstalacion = entrada_nombre_ejecutantes_desinstalacion.get().strip() or None

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE Centros_Cultivo SET NombreCentro = %s, NombrePonton = %s, FechaEntrega = %s, 
            FechaDesinstalacion = %s, NumeroModulo = %s, JaulasPorModulo = %s, MedidasJaula = %s, 
            TipoSistemaVideo = %s, TipoSistemaAlimentacion = %s, NombreEjecutantesInstalacion = %s, 
            NombreEjecutantesDesinstalacion = %s WHERE ID = %s
            """
            valores = (
                nuevo_nombre_centro, nuevo_nombre_ponton, nueva_fecha_entrega, nueva_fecha_desinstalacion,
                nuevo_numero_modulo, nuevas_jaulas_modulo, nuevas_medidas_jaula, nuevo_tipo_video,
                nuevo_tipo_alimentacion, nuevo_nombre_ejecutantes_instalacion, nuevo_nombre_ejecutantes_desinstalacion,
                id_centro
            )
            cursor.execute(sql, valores)
            conexion.commit()
            messagebox.showinfo("Información", "Centro de cultivo actualizado exitosamente")
            mostrar_lista()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar el centro de cultivo: {e}")
        finally:
            conexion.close()

# Función para abrir la ventana de gestión de centros de cultivo
def abrir_ejecutantes():
    ventana_ejecutantes = tk.Toplevel()
    ventana_ejecutantes.title("Gestión Centro de Cultivo")

    # Crear el canvas y la scrollbar para la pestaña
    canvas = tk.Canvas(ventana_ejecutantes)
    scrollbar = tk.Scrollbar(ventana_ejecutantes, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Crear un frame en el canvas para contener los widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Ajustar la barra de desplazamiento cuando se añaden widgets
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Crear y mostrar los widgets para agregar un centro de cultivo
    ttk.Label(frame, text="ID:").grid(row=0, column=0)
    global entrada_id
    entrada_id = ttk.Entry(frame)
    entrada_id.grid(row=0, column=1)

    ttk.Label(frame, text="Nombre del Centro de Cultivo:").grid(row=1, column=0)
    global entrada_nombre_centro
    entrada_nombre_centro = ttk.Entry(frame)
    entrada_nombre_centro.grid(row=1, column=1)

    ttk.Label(frame, text="Nombre del Pontón:").grid(row=2, column=0)
    global entrada_nombre_ponton
    entrada_nombre_ponton = ttk.Entry(frame)
    entrada_nombre_ponton.grid(row=2, column=1)

    ttk.Label(frame, text="Fecha de Entrega (YYYY-MM-DD):").grid(row=3, column=0)
    global entrada_fecha_entrega
    entrada_fecha_entrega = ttk.Entry(frame)
    entrada_fecha_entrega.grid(row=3, column=1)

    ttk.Label(frame, text="Fecha de Desinstalación (YYYY-MM-DD):").grid(row=4, column=0)
    global entrada_fecha_desinstalacion
    entrada_fecha_desinstalacion = ttk.Entry(frame)
    entrada_fecha_desinstalacion.grid(row=4, column=1)

    ttk.Label(frame, text="Número de Módulo:").grid(row=5, column=0)
    global entrada_numero_modulo
    entrada_numero_modulo = ttk.Entry(frame)
    entrada_numero_modulo.grid(row=5, column=1)

    ttk.Label(frame, text="Jaulas por Módulo:").grid(row=6, column=0)
    global entrada_jaulas_modulo
    entrada_jaulas_modulo = ttk.Entry(frame)
    entrada_jaulas_modulo.grid(row=6, column=1)

    ttk.Label(frame, text="Medidas de Jaula:").grid(row=7, column=0)
    global entrada_medidas_jaula
    entrada_medidas_jaula = ttk.Entry(frame)
    entrada_medidas_jaula.grid(row=7, column=1)

    ttk.Label(frame, text="Tipo de Sistema de Video:").grid(row=8, column=0)
    global entrada_tipo_video
    entrada_tipo_video = ttk.Entry(frame)
    entrada_tipo_video.grid(row=8, column=1)

    ttk.Label(frame, text="Tipo de Sistema de Alimentación:").grid(row=9, column=0)
    global entrada_tipo_alimentacion
    entrada_tipo_alimentacion = ttk.Entry(frame)
    entrada_tipo_alimentacion.grid(row=9, column=1)

    ttk.Label(frame, text="Nombre Ejecutantes Instalación:").grid(row=10, column=0)
    global entrada_nombre_ejecutantes_instalacion
    entrada_nombre_ejecutantes_instalacion = ttk.Entry(frame)
    entrada_nombre_ejecutantes_instalacion.grid(row=10, column=1)

    ttk.Label(frame, text="Nombre Ejecutantes Desinstalación:").grid(row=11, column=0)
    global entrada_nombre_ejecutantes_desinstalacion
    entrada_nombre_ejecutantes_desinstalacion = ttk.Entry(frame)
    entrada_nombre_ejecutantes_desinstalacion.grid(row=11, column=1)

    # Botones para agregar, eliminar y actualizar centros de cultivo
    ttk.Button(frame, text="Agregar Centro de Cultivo", command=agregar_centro).grid(row=12, column=0)
    ttk.Button(frame, text="Eliminar Centro de Cultivo", command=eliminar_centro).grid(row=12, column=1)
    ttk.Button(frame, text="Actualizar Centro de Cultivo", command=actualizar_centro).grid(row=13, column=0)

    # Lista para mostrar los centros de cultivo
    global lista
    lista = tk.Listbox(frame)
    lista.grid(row=14, column=0, columnspan=2, sticky="nsew")

    # Llenar la lista al abrir la ventana
    mostrar_lista()

    ventana_ejecutantes.geometry("600x400")

# Función para abrir la ventana principal
def abrir_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Mantención Agua Mar")

    # Crear el menú principal
    menu_bar = tk.Menu(ventana_principal)
    menu_inventario = tk.Menu(menu_bar, tearoff=0)

    menu_inventario.add_command(label="Sistemas de Alimentación", command=abrir_inventario)
    menu_bar.add_cascade(label="Inventario", menu=menu_inventario)

    ventana_principal.config(menu=menu_bar)

    ttk.Button(ventana_principal, text="Gestión Centro de Cultivo", command=abrir_ejecutantes).pack()

    ventana_principal.geometry("400x200")
    ventana_principal.mainloop()

# Función para abrir la ventana de inventario (a completar)
def abrir_inventario():
    pass  # Implementa la lógica para abrir la ventana de inventario

# Función para abrir la ventana de inventario
def abrir_inventario():
    ventana_inventario = tk.Toplevel()
    ventana_inventario.title("Inventario")

    notebook = ttk.Notebook(ventana_inventario)

    def crear_pestaña(nombre):
        frame_pestana = ttk.Frame(notebook)
        notebook.add(frame_pestana, text=nombre)
        tk.Label(frame_pestana, text=f"Información para {nombre}:").pack(pady=10)

        tk.Label(frame_pestana, text="Número de Serie:").pack(pady=5)
        tk.Entry(frame_pestana).pack(pady=5)

        tk.Label(frame_pestana, text="Estado:").pack(pady=5)
        tk.Entry(frame_pestana).pack(pady=5)

        tk.Label(frame_pestana, text="Ubicación:").pack(pady=5)
        tk.Entry(frame_pestana).pack(pady=5)

        tk.Label(frame_pestana, text="Comentarios:").pack(pady=5)
        tk.Entry(frame_pestana).pack(pady=5)

        botones_frame = tk.Frame(frame_pestana)
        botones_frame.pack(pady=10)

        tk.Button(botones_frame, text="Agregar").pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Mostrar").pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Eliminar").pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Actualizar Datos").pack(side=tk.LEFT, padx=5)

    # Crear pestañas para los distintos sistemas
    crear_pestaña("Sistemas de Alimentación")
    crear_pestaña("Sistemas de Monitoreo")
    crear_pestaña("Carro Monitor")
    crear_pestaña("Estación Ambiental")

    notebook.pack(expand=True, fill='both')


# Inicia la aplicación llamando a la ventana principal
if __name__ == "__main__":
    abrir_ventana_principal()
