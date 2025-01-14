import tkinter as tk
import pandas as pd
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
        
        self.data_by_file = {}
        
        for file in files:
            df = pd.read_excel(file)
            self.data_by_file[file] = df
        
        messagebox.showinfo("Info", "Archivos cargados correctamente")
        
    def select_columns(self):
        if not self.data_by_file:
            messagebox.showwarning("Advertencia", "Carga datos primero.")
            return

        select_window = tk.Toplevel(self.root)
        select_window.title("Seleccionar Columnas")

        canvas = tk.Canvas(select_window)
        scrollbar = tk.Scrollbar(select_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", expand=True, fill="both")

        self.selected_columns_by_file = {}

        for file, df in self.data_by_file.items():
            frame = tk.LabelFrame(scrollable_frame, text=f"Campos en {file.split('/')[-1]}")
            frame.pack(fill="both", expand=True, padx=10, pady=5)

            columns = df.columns.tolist()
            var_dict = {col: tk.BooleanVar() for col in columns}

            for col, var in var_dict.items():
                chk = tk.Checkbutton(frame, text=col, variable=var)
                chk.pack(anchor="w")

            self.selected_columns_by_file[file] = var_dict

        button_frame = tk.Frame(select_window)
        button_frame.pack(fill="x", pady=5)
        
        select_window.update_idletasks()  
        canvas.config(scrollregion=canvas.bbox("all"))
        
        tk.Button(button_frame, text="Aceptar", command=lambda: [self.display_selected_data(), select_window.destroy()]).pack(pady=5)


    def display_selected_data(self):
        if not self.selected_columns_by_file:
            messagebox.showwarning("Advertencia", "No seleccionaste columnas.")
            return
        
        combined_data = []
        
        for file, columns in self.selected_columns_by_file.items():
            df = self.data_by_file[file]
            selected_cols = [col for col, var in columns.items() if var.get()]
            if selected_cols:
                filtered_df = df[selected_cols]
                combined_data.append(filtered_df)
        
        if combined_data:
            self.data = pd.concat(combined_data, ignore_index=True)
            self.display_data()
        else:
            messagebox.showinfo("Info", "No se seleccionaron columnas para mostrar.")
        
    def display_data(self):
        if self.data is None:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        columns = self.data.columns.tolist()
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col, )
            self.tree.column(col, width=150) 

        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=row.tolist())
 
    def run(self):
        self.root.mainloop()

        