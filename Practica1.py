import tkinter as tk
from tkinter import ttk
import requests

# Función para obtener recomendaciones basadas en el filtro seleccionado
def obtener_recomendaciones():
    resultado.delete(1.0, tk.END)
    
    # Obtiene el filtro seleccionado por el usuario
    filtro = filtro_combobox.get()
    
    if not filtro:
        return
    
    if filtro == "Estrenos":
        # Obtener películas en cartelera (puedes ajustar los parámetros según sea necesario)
        url = "https://api.themoviedb.org/3/movie/now_playing"
        params = {
            "api_key": "3d16ede65af012c2020d73640a669ddf",  # Reemplaza con tu propia clave API de TMDb
            "language": "es-ES",  # Puedes ajustar el idioma según tu preferencia
            "page": 1
        }
    elif filtro == "Cine de Oro":
        # Obtener películas clásicas de "Cine de Oro" (puedes ajustar los parámetros según sea necesario)
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": "3d16ede65af012c2020d73640a669ddf",  # Reemplaza con tu propia clave API de TMDb
            "language": "es-ES",  # Puedes ajustar el idioma según tu preferencia
            "sort_by": "popularity.desc",
            "release_date.gte": "1900-01-01",
            "release_date.lte": "1960-12-31"
        }
    elif filtro == "Películas Más Conocidas":
        # Obtener películas populares (puedes ajustar los parámetros según sea necesario)
        url = "https://api.themoviedb.org/3/movie/popular"
        params = {
            "api_key": "3d16ede65af012c2020d73640a669ddf",  # Reemplaza con tu propia clave API de TMDb
            "language": "es-ES",  # Puedes ajustar el idioma según tu preferencia
            "page": 1
        }
    else:
        resultado.insert(tk.END, "Filtro no válido.")
        return
    
    # Realizar la solicitud a la API de TMDb
    response = requests.get(url, params=params)
    data = response.json()
    
    # Procesar la respuesta de la API y mostrar las recomendaciones
    if data.get("results"):
        for pelicula in data["results"]:
            titulo = pelicula["title"]
            resultado.insert(tk.END, f'Título: {titulo}\n')
    else:
        resultado.insert(tk.END, "No se encontraron recomendaciones para este filtro.")

# Función para obtener recomendaciones por género
def obtener_recomendaciones_genero():
    resultado.delete(1.0, tk.END)
    
    # Obtiene el género seleccionado por el usuario
    genero = genero_combobox.get()
    
    if not genero:
        return
    
    # Hacer una solicitud a la API de TMDb para obtener recomendaciones por género
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": "3d16ede65af012c2020d73640a669ddf",  # Reemplaza con tu propia clave API de TMDb
        "language": "es-ES",  # Puedes ajustar el idioma según tu preferencia
        "sort_by": "popularity.desc",
        "with_genres": genero
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Procesar la respuesta de la API y mostrar las recomendaciones por género
    if data.get("results"):
        for pelicula in data["results"]:
            titulo = pelicula["title"]
            resultado.insert(tk.END, f'Título: {titulo}\n')
    else:
        resultado.insert(tk.END, "No se encontraron recomendaciones para este género.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Recomendación de Películas")

# Crear pestañas (tabs) para organizar los filtros
pestañas = ttk.Notebook(ventana)

# Pestaña para los filtros por género
pestaña_genero = ttk.Frame(pestañas)
pestañas.add(pestaña_genero, text="Filtro por Género")

# Etiqueta para el género
etiqueta_genero = tk.Label(pestaña_genero, text="Selecciona un género:")
etiqueta_genero.pack()

# Combobox para seleccionar el género
generos_disponibles = ["Acción", "Comedia", "Terror", "Drama", "Romance"]
genero_combobox = ttk.Combobox(pestaña_genero, values=generos_disponibles)
genero_combobox.pack()

# Botón para obtener recomendaciones por género
boton_recomendaciones_genero = tk.Button(pestaña_genero, text="Obtener Recomendaciones", command=obtener_recomendaciones_genero)
boton_recomendaciones_genero.pack()

# Pestaña para los filtros adicionales
pestaña_filtros_adicionales = ttk.Frame(pestañas)
pestañas.add(pestaña_filtros_adicionales, text="Filtros Adicionales")

# Etiqueta para el filtro
etiqueta_filtro = tk.Label(pestaña_filtros_adicionales, text="Selecciona un filtro adicional:")
etiqueta_filtro.pack()

# Combobox para seleccionar el filtro adicional
filtros_adicionales = ["Estrenos", "Cine de Oro", "Películas Más Conocidas"]
filtro_combobox = ttk.Combobox(pestaña_filtros_adicionales, values=filtros_adicionales)
filtro_combobox.pack()

# Botón para obtener recomendaciones basadas en el filtro adicional
boton_recomendaciones = tk.Button(pestaña_filtros_adicionales, text="Obtener Recomendaciones", command=obtener_recomendaciones)
boton_recomendaciones.pack()

# Cuadro de texto para mostrar las recomendaciones
resultado = tk.Text(ventana, width=40, height=10)
resultado.pack()

# Agregar las pestañas a la ventana
pestañas.pack()

# Iniciar la aplicación
ventana.mainloop()
