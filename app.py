import tkinter as tk
from tkinter import ttk
from Modelling import ModelingTab
from Uji_Data import UjiDataTab

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEM PENDUKUNG KEPUTUSAN KELAYAKAN PENERIMA BEASISWA MENGGUNAKAN ALGORITMA RANDOM FOREST")
        self.root.geometry("1000x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Inisialisasi tab
        self.modeling_tab = ModelingTab(self.notebook)
        self.uji_data_tab = UjiDataTab(self.notebook, self.modeling_tab)  # Menerima objek ModelingTab

        # Menambahkan tab ke notebook
        self.notebook.add(self.modeling_tab.frame, text="Modeling")
        self.notebook.add(self.uji_data_tab.frame, text="Uji Data")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

        
