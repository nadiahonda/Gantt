import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from gantt_chart import generate_gantt_chart

class GanttChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gantt Chart")
        self.root.geometry("350x450")  # Largura x Altura
        # self.root.iconbitmap('data/icon.ico') #define icon
        self.file_path = tk.StringVar()
        self.include_fp = tk.BooleanVar()  # Variável para o toggle "hide F&P"
        self.time_unit = tk.StringVar(value="min")  # Variável para a unidade de tempo
        self.fig = None  # Store the figure

        # Dicionário de cores iniciais
        self.batch_colors = {
            1: 'Light Green',
            2: 'Dark Green',
            3: 'Dark Blue',
            4: 'Dark Orange',
            5: 'None',
            6: 'None',
            7: 'None',
            8: 'None',
        }

        self.color_options = {
            'None': None,
            'Light Green': '#AAB400',
            'Dark Green': '#5F7800',
            'Light Blue': '#82C8DC',
            'Dark Blue': '#00A0BE',
            'Light Orange': '#FFB400',
            'Dark Orange': '#EB8200',
            'Light Gray': '#D9D5D2',
            'Dark Gray': '#333333'
        }

        self.create_widgets()

    def create_widgets(self):
        # Alinhando o texto à esquerda e organizando os widgets com o gerenciador de layout grid
        tk.Label(self.root, text="Select Excel File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Entry(self.root, textvariable=self.file_path, width=23).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Button(self.root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        # Adicionando a divisória horizontal
        ttk.Separator(self.root, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Adicionando comboboxes para seleção de cores
        for i, batch in enumerate(self.batch_colors.keys(), start=2):
            tk.Label(self.root, text=f"Batch {batch} color:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            combobox = ttk.Combobox(self.root, values=list(self.color_options.keys()), state="readonly")
            combobox.set(self.batch_colors[batch])
            combobox.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            combobox.bind("<<ComboboxSelected>>", lambda event, b=batch: self.update_color(b, event.widget.get()))

        # Adicionando o toggle "include F&P"
        tk.Checkbutton(self.root, text="Include F&P (if existing)", variable=self.include_fp).grid(row=i+1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Adicionando a divisória horizontal
        ttk.Separator(self.root, orient='horizontal').grid(row=i+2, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Adicionando o campo de entrada para a unidade de tempo
        tk.Label(self.root, text="Time unit:").grid(row=i+3, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.time_unit, width=10).grid(row=i+3, column=1, padx=10, pady=5, sticky="w")

        # Colocando os botões na mesma linha
        tk.Button(self.root, text="Gantt Chart", command=self.generate_chart).grid(row=i+4, column=0, padx=10, pady=5, sticky="w")
        tk.Button(self.root, text="PNG Save", command=self.save_chart).grid(row=i+4, column=1, padx=10, pady=5, sticky="e")

    def update_color(self, batch, color_name):
        self.batch_colors[batch] = color_name

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.file_path.set(file_path)

    def generate_chart(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select an Excel file")
            return

        try:
            df = pd.read_excel(file_path, sheet_name='Gantt')  # Especifica a aba "Gantt"
            
            # Verifica se todas as colunas necessárias estão presentes
            required_columns = {'Start', 'Duration', 'Batch', 'Resource 1', 'Resource 2', 'Resource 3'}
            if not required_columns.issubset(df.columns):
                missing_cols = required_columns - set(df.columns)
                raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
            
            custom_colors = {batch: self.color_options[color_name] for batch, color_name in self.batch_colors.items() if color_name != 'None'}
            self.fig = generate_gantt_chart(df, custom_colors, include_fp=self.include_fp.get(), time_unit=self.time_unit.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_chart(self):
        if self.fig is None:
            messagebox.showerror("Error", "Please generate a Gantt chart first")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.fig.savefig(file_path, transparent=True)
            messagebox.showinfo("Success", "Gantt chart saved successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()