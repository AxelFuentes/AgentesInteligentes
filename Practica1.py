import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

# Diccionario de películas con géneros como características y rutas de imagen
movies = {
    # Películas existentes
    "Avengers End Game": {
        "genres": ["Accion", "Ciencia Ficcion"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\AvengersEndGame.jpg"
    },
    "El diario de una pasion": {
        "genres": ["Drama", "Romance"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\ElDiario.jpg"
    },
    "Harry Potter y la Camara Secreta": {
        "genres": ["Aventura", "Fantasia"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\HarryCamaraSecreta.jpg"
    },
    "Una Esposa de Mentira": {
        "genres": ["Comedia", "Romance"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\EsposaMentira.jpg"
    },
    "Apocalypto": {
        "genres": ["Accion", "Aventura"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\Apocalypto.jpg"
    },
    "Ruega Por Nosotros": {
        "genres": ["Terror", "Suspenso"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\RuegaPorNosotros.jpg"
    },
    "Nunca Digas su Nombre": {
        "genres": ["Terror", "Suspenso", "Accion"],
        "image_path": r"C:\Users\HP\Documents\ESIME Zacatenco\9no Semestre\Agentes Inteligentes Expertos\Programas\Practcia1\NuncaDigasNombre.jpg"
    },
}

# Lista de nombres de películas recomendadas (limitadas a 6 películas)
recommended_movies = list(movies.keys())[:6]

# Clase para el motor de recomendación de películas basado en contenido
class ContentBasedRecommender:
    def __init__(self):
        # Diccionario de películas con géneros como características y rutas de imagen
        self.movies = movies  # Usamos el mismo diccionario de películas

    def get_recommendations(self, selected_movies):
        # Calcular los géneros seleccionados
        selected_genres = set()
        for movie in selected_movies:
            if movie in self.movies:
                selected_genres.update(self.movies[movie]["genres"])

        # Calcular la similitud de género con otras películas y obtener las recomendaciones
        recommendations = []
        for movie, data in self.movies.items():
            if movie not in selected_movies:
                common_genres = set(data["genres"]).intersection(selected_genres)
                similarity = len(common_genres) / len(selected_genres)
                recommendations.append((movie, similarity))

        # Ordenar películas por similitud descendente
        recommendations.sort(key=lambda x: x[1], reverse=True)

        # Retornar las películas más similares (hasta 3) que tienen similitud mayor a cero
        filtered_recommendations = [movie for movie, sim in recommendations if sim > 0]
        return filtered_recommendations

# Variable global para rastrear la ventana de "Recomendaciones"
recommendations_window = None

# Crear la ventana principal
root = tk.Tk()
root.title("Selección de Películas")

# Crear un marco para organizar las imágenes en una cuadrícula
image_frame = ttk.Frame(root)
image_frame.pack()

# Función para manejar la selección de películas
def on_movie_select(movie):
    update_image_display(movie)

# Función para actualizar la visualización de imágenes seleccionadas
def update_image_display(movie):
    img = Image.open(movies[movie]["image_path"])
    tk_img = ImageTk.PhotoImage(img)

    # Si la película está seleccionada, aplicar un borde resaltado
    if selected_movies[movie].get():
        image_labels[movie].config(image=tk_img, borderwidth=3, relief="solid")
        image_labels[movie].img = tk_img
    else:
        image_labels[movie].config(image=tk_img, borderwidth=0)
        image_labels[movie].img = tk_img

# Lista para rastrear películas seleccionadas
selected_movies = {movie: tk.BooleanVar() for movie in recommended_movies}
for movie in recommended_movies:
    selected_movies[movie].set(False)

# Crear etiquetas de imagen y casillas de verificación para mostrar las portadas de las películas en una cuadrícula
image_labels = {}
checkboxes = {}
rows = 2  # Número de filas
columns = 3  # Número de columnas
current_row = 0
current_column = 0

for movie in recommended_movies:
    img = Image.open(movies[movie]["image_path"])
    tk_img = ImageTk.PhotoImage(img)

    image_label = ttk.Label(image_frame, image=tk_img)
    image_label.img = tk_img

    select_checkbox = ttk.Checkbutton(image_frame, text=movie, variable=selected_movies[movie],
                                     command=lambda movie=movie: on_movie_select(movie))

    image_labels[movie] = image_label

    image_label.grid(row=current_row, column=current_column, padx=10, pady=10)
    select_checkbox.grid(row=current_row + 1, column=current_column, padx=10, pady=10)

    current_column += 1
    if current_column >= columns:
        current_column = 0
        current_row += 2

# Función para obtener películas recomendadas y mostrarlas en una nueva ventana
def show_recommendations():
    global recommendations_window  # Usar la variable global

    # Cerrar la ventana de "Recomendaciones" si está abierta
    if recommendations_window:
        recommendations_window.destroy()

    selected = [movie for movie, var in selected_movies.items() if var.get()]
    recommendations = ContentBasedRecommender().get_recommendations(selected)
    
    if not recommendations:
        messagebox.showinfo("Sin recomendaciones", "No se encontraron recomendaciones para las películas seleccionadas.")
    else:
        # Crear una nueva ventana para mostrar las recomendaciones
        recommendations_window = tk.Toplevel(root)
        recommendations_window.title("Recomendaciones")
        
        # Crear un marco para organizar las imágenes en una cuadrícula en la nueva ventana
        recommendations_frame = ttk.Frame(recommendations_window)
        recommendations_frame.pack()

        # Crear etiquetas de imagen y texto para mostrar las recomendaciones
        recommendations_labels = {}
        rows = 2  # Número de filas
        columns = 3  # Número de columnas
        current_row = 0
        current_column = 0

        for movie in recommendations:
            img = Image.open(movies[movie]["image_path"])
            tk_img = ImageTk.PhotoImage(img)

            recommendations_label = ttk.Label(recommendations_frame, image=tk_img, text=movie, compound=tk.TOP)
            recommendations_label.img = tk_img

            recommendations_labels[movie] = recommendations_label

            recommendations_label.grid(row=current_row, column=current_column, padx=10, pady=10)

            current_column += 1
            if current_column >= columns:
                current_column = 0
                current_row += 1

# Botón para obtener películas recomendadas y mostrarlas en una nueva ventana
recommend_button = ttk.Button(root, text="Mostrar Recomendaciones", command=show_recommendations)
recommend_button.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
