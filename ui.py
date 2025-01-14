import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from file_handler import load_files
from data_analyzer import filter_data

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Excel Analyzer")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")

        self.data = None
        self.selected_columns = []
        
        tk.Button(self.root, text="Cargar Excel", command=self.load_excel).pack(pady=10)
        tk.Button(self.root, text="Seleccionar Columnas", command=self.select_columns).pack(pady=10)
        
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        
    def load_excel(self):
        files = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not files:
            messagebox.showwarning("Advertencia", "No se seleccionaron archivos")
            return
        
        self.data = load_files(files)
        
        
        messagebox.showinfo("Info", "Archivos cargados correctamente")
        
    def select_columns(self):
        if self.data is None:
            messagebox.showwarning("Advertencia", "Carga datos primero.")
            return
        
        columns_window = tk.Toplevel(self.root)
        columns_window.title("Seleccionar Columnas")

        canvas = tk.Canvas(columns_window)
        scrollbar = tk.Scrollbar(columns_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", expand=True, fill="both")

        columns = list(self.data.columns)
        var = [tk.BooleanVar(value=False) for _ in columns]

        for i, col in enumerate(columns):
            tk.Checkbutton(frame, text=col, variable=var[i]).pack(anchor="w")

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        def save_selection():
            self.selected_columns = [columns[i] for i in range(len(columns)) if var[i].get()]
            columns_window.destroy()
            self.display_data()

        tk.Button(columns_window, text="Aceptar", command=save_selection).pack(pady=10)

    def display_data(self):
        if not self.selected_columns:
            messagebox.showwarning("Advertencia", "No seleccionaste columnas.")
            return
        
        filtered_data = filter_data(self.data, self.selected_columns)

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = self.selected_columns
        self.tree["show"] = "headings"

        for col in self.selected_columns:
            self.tree.heading(col, text=col)

        for _, row in filtered_data.iterrows():
            self.tree.insert("", "end", values=list(row))

    
    
    def run(self):
        self.root.mainloop()

        