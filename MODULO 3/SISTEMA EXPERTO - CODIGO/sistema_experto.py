import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import ast

# Cargar el dataset
df = pd.read_csv("RAW_recipes.csv")

# Convertir los nombres de las recetas a mayúsculas
df["name"] = df["name"].str.upper()

# Preprocesar columnas
df = df.dropna(subset=["description", "tags", "minutes", "name", "ingredients", "steps"])
df["tags"] = df["tags"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["ingredients"] = df["ingredients"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["steps"] = df["steps"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")

# Mapas de equivalencia
platillos_en = {
    "Entrada": "appetizers",
    "Plato fuerte": "main-dish",
    "Postre": "desserts",
    "Desayuno": "breakfast",
    "Merienda": "snacks",
    "Almuerzo": "lunch",
    "Bebida": "beverages"
}

dietas_en = {
    "Vegetariana": "vegetarian",
    "Vegana": "vegan",
    "Sin gluten": "gluten-free",
    "Baja en calorías": "low-calorie",
    "Alta en proteína": "high-protein",
    "Bajo en sodio": "low-sodium",
    "Sin azúcar": "sugar-free"
}

# Diccionario de equivalencias para ingredientes con múltiples términos
ingredientes_en = {
    "Huevo": ["egg", "eggs"],
    "Papa": ["potato", "potatoes"],
    "Arroz": ["rice"],
    "Tomate": ["tomato", "crushed tomatoes", "tomatoes", "diced tomatoes"],
    "Pollo": ["chicken"],
    "Lenteja": ["lentil", "lentils"],
    "Espinaca": ["spinach"],
    "Champiñones": ["mushroom", "mushrooms"],
    "Zanahoria": ["carrot", "carrots"],
    "Calabaza": ["pumpkin", "squash","pumpkins"]
}

# Función para filtrar por ingredientes
def filtrar_por_ingredientes(ingredientes):
    # Traducir los ingredientes seleccionados al inglés (múltiples términos)
    ingredientes_traducidos = []
    for ing in ingredientes:
        if ing in ingredientes_en:
            ingredientes_traducidos.append(ingredientes_en[ing])  # Agregar todos los términos asociados como lista
        else:
            ingredientes_traducidos.append([ing.lower()])  # Si no está en el diccionario, usar el término original como lista

    # Filtrar recetas que contengan al menos uno de los valores traducidos para cada ingrediente seleccionado
    def cumple_ingredientes(ingredientes_receta):
        return all(
            any(term.lower() in map(str.lower, ingredientes_receta) for term in grupo)
            for grupo in ingredientes_traducidos
        )

    return df[df["ingredients"].apply(cumple_ingredientes)]

# Función para filtrar guiado
def filtrar_guiado(platillo, dieta, tiempo):
    filtrado = df.copy()
    if platillo:
        tag_ingles = platillos_en.get(platillo, "").lower()
        filtrado = filtrado[filtrado["tags"].apply(lambda t: tag_ingles in map(str.lower, t))]
    if dieta:
        tag_ingles = dietas_en.get(dieta, "").lower()
        filtrado = filtrado[filtrado["tags"].apply(lambda t: tag_ingles in map(str.lower, t))]
    if tiempo:
        if tiempo == "Menos de 15 min": filtrado = filtrado[filtrado["minutes"] < 15]
        elif tiempo == "Menos de 30 min": filtrado = filtrado[filtrado["minutes"] < 30]
        elif tiempo == "Menos de 60 min": filtrado = filtrado[filtrado["minutes"] < 60]
        elif tiempo == "Más de 60 min": filtrado = filtrado[filtrado["minutes"] > 60]
    return filtrado

# Interfaz gráfica
class SistemaExpertoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto de Recetas")
        self.root.geometry("400x400")  # Tamaño de la ventana principal
        self.opcion = tk.StringVar()

        ttk.Label(root, text="¿Cómo quieres buscar recetas?").pack(pady=10)
        ttk.Radiobutton(root, text="Por ingredientes", variable=self.opcion, value="ingredientes").pack()
        ttk.Radiobutton(root, text="Búsqueda guiada", variable=self.opcion, value="guiada").pack()
        ttk.Button(root, text="Continuar", command=self.continuar).pack(pady=10)

    def continuar(self):
        if self.opcion.get() == "ingredientes":
            self.ventana_ingredientes()
        elif self.opcion.get() == "guiada":
            self.ventana_guiada()
        else:
            messagebox.showwarning("Atención", "Selecciona una opción.")

    def ventana_ingredientes(self):
        top = tk.Toplevel(self.root)
        top.title("Busqueda por ingredientes")
        top.geometry("300x280")  # Tamaño de la ventana de selección de ingredientes
        seleccionados = {}
        ingredientes = ["Huevo", "Papa", "Arroz", "Tomate", "Pollo", "Lenteja", "Espinaca", "Champiñones", "Zanahoria", "Calabaza"]
        for ingr in ingredientes:
            var = tk.BooleanVar()
            ttk.Checkbutton(top, text=ingr, variable=var).pack(anchor="w")
            seleccionados[ingr] = var

        def buscar():
            elegidos = [i for i, v in seleccionados.items() if v.get()]
            if not elegidos: return messagebox.showinfo("Info", "Selecciona al menos un ingrediente")
            resultados = filtrar_por_ingredientes(elegidos)
            self.mostrar_resultados(resultados)

        ttk.Button(top, text="Buscar", command=buscar).pack(pady=10)

    def ventana_guiada(self):
        top = tk.Toplevel(self.root)
        top.title("Búsqueda guiada")
        top.geometry("300x600")  # Tamaño de la ventana de búsqueda guiada
        platillo_var = tk.StringVar()
        dieta_var = tk.StringVar()
        tiempo_var = tk.StringVar()

        ttk.Label(top, text="Platillo:").pack()
        for p in platillos_en.keys():
            ttk.Radiobutton(top, text=p, variable=platillo_var, value=p).pack(anchor="w")

        ttk.Label(top, text="Dieta:").pack()
        for d in dietas_en.keys():
            ttk.Radiobutton(top, text=d, variable=dieta_var, value=d).pack(anchor="w")

        ttk.Label(top, text="Tiempo:").pack()
        for t in ["Menos de 15 min", "Menos de 30 min", "Menos de 60 min", "Más de 60 min"]:
            ttk.Radiobutton(top, text=t, variable=tiempo_var, value=t).pack(anchor="w")

        def buscar():
            resultados = filtrar_guiado(platillo_var.get(), dieta_var.get(), tiempo_var.get())
            self.mostrar_resultados(resultados)

        ttk.Button(top, text="Buscar", command=buscar).pack(pady=10)

    def mostrar_resultados(self, recetas):
        top = tk.Toplevel(self.root)
        top.title("Recetas encontradas")
        top.geometry("1200x700")  # Tamaño de la ventana de resultados

        if recetas.empty:
            ttk.Label(top, text="No se encontraron recetas").pack()
            return

        # Mostrar el total de resultados
        total_resultados = len(recetas)
        ttk.Label(top, text=f"Total de resultados: {total_resultados}", font=("Arial", 12, "bold")).pack(pady=10)

        # Configurar el Treeview con las columnas adicionales
        tree = ttk.Treeview(top, columns=("Nombre", "Minutos", "Ingredientes", "Pasos"), show="headings")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Minutos", text="Minutos")
        tree.heading("Ingredientes", text="Ingredientes")
        tree.heading("Pasos", text="Pasos")
        tree.pack(side="left", fill="y", padx=10, pady=10)

        # Crear un área para mostrar los detalles de la receta seleccionada
        detalles_frame = ttk.LabelFrame(top, text="Detalles de la receta", padding=(10, 10))
        detalles_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        detalles_text = tk.Text(detalles_frame, wrap="word", state="disabled", font=("Arial", 12))
        detalles_text.pack(fill="both", expand=True)

        # Insertar los datos en el Treeview
        for _, row in recetas.iterrows():
            # Obtener los ingredientes y pasos como cadenas
            ingredientes = ", ".join(row["ingredients"]) if isinstance(row["ingredients"], list) else "No disponible"
            pasos = " | ".join(row["steps"]) if isinstance(row["steps"], list) else "No disponible"

            # Insertar los datos en el Treeview
            tree.insert("", "end", values=(row["name"], int(row["minutes"]), ingredientes, pasos))

        # Función para mostrar detalles de la receta seleccionada
        def mostrar_detalles(event):
            # Obtener el elemento seleccionado
            item = tree.selection()
            if not item:
                return
            receta_seleccionada = tree.item(item, "values")

            # Mostrar los detalles en el área de texto
            detalles_text.config(state="normal")
            detalles_text.delete("1.0", tk.END)  # Limpiar el área de texto
            detalles_text.insert(tk.END, f"Nombre: {receta_seleccionada[0]}\n")
            detalles_text.insert(tk.END, f"Tiempo: {receta_seleccionada[1]} minutos\n\n")
            detalles_text.insert(tk.END, "Ingredientes:\n")
            detalles_text.insert(tk.END, f"{receta_seleccionada[2]}\n\n")
            detalles_text.insert(tk.END, "Pasos:\n")

            # Formatear los pasos como una lista numerada
            pasos_lista = receta_seleccionada[3].split(" | ") if receta_seleccionada[3] != "No disponible" else []
            for i, paso in enumerate(pasos_lista, 1):
                detalles_text.insert(tk.END, f"{i}. {paso}\n")

            detalles_text.config(state="disabled")  # Deshabilitar edición

        # Vincular el evento de selección al Treeview
        tree.bind("<<TreeviewSelect>>", mostrar_detalles)

# Ejecutar
root = tk.Tk()
app = SistemaExpertoApp(root)
root.mainloop()
