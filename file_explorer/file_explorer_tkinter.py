import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import psutil

class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Explorador de Archivos")
        self.geometry("800x600")
        self.configure(bg="white")

        # Cargar imágenes
        self.disk_icon = self.load_image("disk.png", (20, 20))  # Icono de disco
        self.folder_icon = self.load_image("folder.png", (20, 20))  # Icono de carpeta
        self.file_icon = self.load_image("file.png", (20, 20))  # Icono de archivo

        # Botón para seleccionar directorio
        self.button = tk.Button(self, text="Seleccionar Directorio", command=self.on_folder_clicked)
        self.button.pack(pady=10)

        # TreeView para mostrar archivos y directorios
        self.treeview = ttk.Treeview(self, columns=("Tipo"), show="tree headings")
        self.treeview.heading("#0", text="Nombre")
        self.treeview.heading("Tipo", text="Tipo")
        self.treeview.column("#0", width=600)
        self.treeview.column("Tipo", width=150)
        self.treeview.pack(expand=True, fill="both", padx=10, pady=10)

        # Evento para expandir nodos
        self.treeview.bind("<ButtonRelease-1>", self.on_treeview_expand)

        # Mostrar unidades de disco al inicio
        self.show_drives()

    def load_image(self, path, size):
        """Cargar y redimensionar una imagen."""
        if not os.path.exists(path):
            return None  # Evitar errores si la imagen no está disponible
        image = Image.open(path)
        image = image.resize(size)
        return ImageTk.PhotoImage(image)

    def show_drives(self):
        """Detectar y mostrar las unidades de disco disponibles."""
        self.treeview.delete(*self.treeview.get_children())  # Limpiar TreeView
        drives = [dp.device for dp in psutil.disk_partitions() if os.path.exists(dp.device)]
        for drive in drives:
            node = self.treeview.insert("", "end", text=drive, values=("Unidad"), image=self.disk_icon, open=False)
            self.treeview.insert(node, "end", text="dummy")  # Nodo ficticio

    def on_folder_clicked(self):
        """Abrir diálogo para seleccionar directorio."""
        folder = filedialog.askdirectory()
        if folder:
            #self.treeview.delete(*self.treeview.get_children())  # Limpiar TreeView
            self.explore_folder(folder, "", folder)

    def explore_folder(self, folder, parent, base_path):
        """Recorrer el directorio y agregar elementos al TreeView."""
        for name in os.listdir(folder):
            full_path = os.path.join(folder, name)
            if os.path.isdir(full_path):
                node = self.treeview.insert(
                    parent, "end", text=name, values=("Directorio"), image=self.folder_icon, open=False
                )
                self.treeview.insert(node, "end", text="dummy")  # Nodo ficticio
            else:
                self.treeview.insert(
                    parent, "end", text=name, values=("Archivo"), image=self.file_icon
                )

    def on_treeview_expand(self, event):
        """Expandir directorio al hacer clic en el botón "+"."""
        item = self.treeview.focus()
        if not item:
            return

        if self.treeview.get_children(item):
            first_child = self.treeview.get_children(item)[0]
            if self.treeview.item(first_child, "text") == "dummy":
                self.treeview.delete(first_child)
                full_path = self.treeview.item(item, "text")
                if os.path.isdir(full_path):
                    self.explore_folder(full_path, item, full_path)

if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
