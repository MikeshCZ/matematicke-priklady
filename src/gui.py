#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from main import generate_sheet


class MathGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generátor matematických příkladů")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Nastavení padding pro celý frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Titulek aplikace
        title_label = ttk.Label(
            main_frame,
            text="Generátor matematických příkladů",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Operace
        row = 1
        ttk.Label(main_frame, text="Operace:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        row += 1

        ops_frame = ttk.Frame(main_frame)
        ops_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        self.op_add = tk.BooleanVar(value=True)
        self.op_sub = tk.BooleanVar(value=True)
        self.op_mul = tk.BooleanVar(value=True)
        self.op_div = tk.BooleanVar(value=True)

        ttk.Checkbutton(ops_frame, text="Sčítání (+)", variable=self.op_add).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 20)
        )
        ttk.Checkbutton(ops_frame, text="Odčítání (-)", variable=self.op_sub).grid(
            row=0, column=1, sticky=tk.W, padx=(0, 20)
        )
        ttk.Checkbutton(ops_frame, text="Násobení (×)", variable=self.op_mul).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(5, 0)
        )
        ttk.Checkbutton(ops_frame, text="Dělení (÷)", variable=self.op_div).grid(
            row=1, column=1, sticky=tk.W, pady=(5, 0)
        )

        row += 2

        # Maximální výsledek
        ttk.Label(main_frame, text="Maximální výsledek:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.max_result = tk.IntVar(value=20)
        max_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=1000, textvariable=self.max_result, width=20
        )
        max_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Počet příkladů
        ttk.Label(main_frame, text="Počet příkladů:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.count = tk.IntVar(value=78)
        count_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=500, textvariable=self.count, width=20
        )
        count_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Počet sloupců
        ttk.Label(main_frame, text="Počet sloupců:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.cols = tk.IntVar(value=3)
        cols_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=10, textvariable=self.cols, width=20
        )
        cols_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Způsob vyplňování
        ttk.Label(main_frame, text="Způsob vyplňování:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.fill_mode = tk.StringVar(value="down")
        fill_frame = ttk.Frame(main_frame)
        fill_frame.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Radiobutton(
            fill_frame, text="Po sloupcích", variable=self.fill_mode, value="down"
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Radiobutton(
            fill_frame, text="Po řádcích", variable=self.fill_mode, value="across"
        ).grid(row=0, column=1, sticky=tk.W)
        row += 1

        # Titulek
        ttk.Label(main_frame, text="Titulek:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.title_text = tk.StringVar(value="Matematické příklady")
        title_entry = ttk.Entry(main_frame, textvariable=self.title_text, width=35)
        title_entry.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Seed (volitelný)
        ttk.Label(main_frame, text="Seed (volitelný):").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.seed = tk.StringVar(value="")
        seed_entry = ttk.Entry(main_frame, textvariable=self.seed, width=35)
        seed_entry.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Label(
            main_frame,
            text="(ponechte prázdné pro náhodné generování)",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=row+1, column=1, sticky=tk.W, pady=(0, 10))
        row += 2

        # Výstupní soubor
        ttk.Label(main_frame, text="Výstupní soubor:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 15)
        )
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=(0, 15))

        self.output_file = tk.StringVar(value="priklady.xlsx")
        file_entry = ttk.Entry(file_frame, textvariable=self.output_file, width=25)
        file_entry.grid(row=0, column=0, sticky=tk.W)

        browse_button = ttk.Button(
            file_frame, text="Procházet...", command=self.browse_file, width=12
        )
        browse_button.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        row += 1

        # Tlačítko Generovat
        generate_button = ttk.Button(
            main_frame,
            text="Generovat příklady",
            command=self.generate,
            width=30
        )
        generate_button.grid(row=row, column=0, columnspan=2, pady=(15, 0))

        # Konfigurace gridu
        main_frame.columnconfigure(1, weight=1)

    def browse_file(self):
        """Otevře dialog pro výběr umístění souboru."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel soubory", "*.xlsx"), ("Všechny soubory", "*.*")],
            initialfile=self.output_file.get()
        )
        if filename:
            self.output_file.set(filename)

    def generate(self):
        """Vygeneruje příklady podle zadaných parametrů."""
        try:
            # Sestavení operací
            ops = []
            if self.op_add.get():
                ops.append("+")
            if self.op_sub.get():
                ops.append("-")
            if self.op_mul.get():
                ops.append("*")
            if self.op_div.get():
                ops.append("/")

            if not ops:
                messagebox.showerror(
                    "Chyba",
                    "Musíte vybrat alespoň jednu operaci!"
                )
                return

            # Získání seed
            seed_value = None
            if self.seed.get().strip():
                try:
                    seed_value = int(self.seed.get().strip())
                except ValueError:
                    messagebox.showerror(
                        "Chyba",
                        "Seed musí být celé číslo!"
                    )
                    return

            # Získání ostatních hodnot
            max_result = self.max_result.get()
            count = self.count.get()
            cols = self.cols.get()
            fill_mode = self.fill_mode.get()
            title = self.title_text.get()
            output_file = self.output_file.get()

            # Validace
            if max_result < 1:
                messagebox.showerror("Chyba", "Maximální výsledek musí být alespoň 1!")
                return

            if count < 1:
                messagebox.showerror("Chyba", "Počet příkladů musí být alespoň 1!")
                return

            if cols < 1:
                messagebox.showerror("Chyba", "Počet sloupců musí být alespoň 1!")
                return

            if not output_file:
                messagebox.showerror("Chyba", "Musíte zadat výstupní soubor!")
                return

            # Generování
            file_path = generate_sheet(
                ops=ops,
                max_result=max_result,
                count=count,
                file_name=output_file,
                seed=seed_value,
                title=title if title else None,
                cols=cols,
                fill_mode=fill_mode
            )

            # Zobrazení úspěšné zprávy
            messagebox.showinfo(
                "Hotovo",
                f"Příklady byly úspěšně vygenerovány!\n\nSoubor: {file_path}"
            )

            # Nabídka otevření souboru
            if messagebox.askyesno("Otevřít soubor?", "Chcete soubor otevřít?"):
                self.open_file(file_path)

        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba při generování:\n{str(e)}")

    def open_file(self, file_path):
        """Otevře vygenerovaný soubor."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS a Linux
                import subprocess
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.call(['open', file_path])
                else:  # Linux
                    subprocess.call(['xdg-open', file_path])
        except Exception as e:
            messagebox.showwarning(
                "Upozornění",
                f"Nepodařilo se otevřít soubor:\n{str(e)}\n\nSoubor najdete v: {file_path}"
            )


def main():
    root = tk.Tk()
    app = MathGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
