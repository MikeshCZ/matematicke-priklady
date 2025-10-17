#!/usr/bin/env python3
"""
GUI aplikace pro generovani matematickych prikladu.
Poskytuje graficke rozhrani pro vsechny funkce generatoru.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from main import generate_sheet


class MathGeneratorGUI:
    """GUI aplikace pro generovani matematickych prikladu."""

    def __init__(self, root):
        """
        Inicializuje GUI aplikaci.

        Args:
            root: Korenovy tkinter widget
        """
        self.root = root
        self.root.title("Generator matematickych prikladu")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Vytvoreni hlavniho framu s paddingem
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Titulek aplikace
        title_label = ttk.Label(
            main_frame,
            text="Generator matematickych prikladu",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Sekce operaci
        row = 1
        ttk.Label(main_frame, text="Operace:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        row += 1

        ops_frame = ttk.Frame(main_frame)
        ops_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Checkboxy pro vyber operaci
        self.op_add = tk.BooleanVar(value=True)
        self.op_sub = tk.BooleanVar(value=True)
        self.op_mul = tk.BooleanVar(value=True)
        self.op_div = tk.BooleanVar(value=True)

        ttk.Checkbutton(ops_frame, text="Scitani (+)", variable=self.op_add).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 20)
        )
        ttk.Checkbutton(ops_frame, text="Odcitani (-)", variable=self.op_sub).grid(
            row=0, column=1, sticky=tk.W, padx=(0, 20)
        )
        ttk.Checkbutton(ops_frame, text="Nasobeni (x)", variable=self.op_mul).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(5, 0)
        )
        ttk.Checkbutton(ops_frame, text="Deleni (/)", variable=self.op_div).grid(
            row=1, column=1, sticky=tk.W, pady=(5, 0)
        )

        row += 2

        # Maximalni vysledek
        ttk.Label(main_frame, text="Maximalni vysledek:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.max_result = tk.IntVar(value=20)
        max_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=1000, textvariable=self.max_result, width=20
        )
        max_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Pocet prikladu
        ttk.Label(main_frame, text="Pocet prikladu:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.count = tk.IntVar(value=78)
        count_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=500, textvariable=self.count, width=20
        )
        count_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Pocet sloupcu
        ttk.Label(main_frame, text="Pocet sloupcu:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.cols = tk.IntVar(value=3)
        cols_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=10, textvariable=self.cols, width=20
        )
        cols_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Zpusob vyplnovani
        ttk.Label(main_frame, text="Zpusob vyplnovani:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.fill_mode = tk.StringVar(value="down")
        fill_frame = ttk.Frame(main_frame)
        fill_frame.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Radiobutton(
            fill_frame, text="Po sloupcich", variable=self.fill_mode, value="down"
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Radiobutton(
            fill_frame, text="Po radcich", variable=self.fill_mode, value="across"
        ).grid(row=0, column=1, sticky=tk.W)
        row += 1

        # Titulek
        ttk.Label(main_frame, text="Titulek:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.title_text = tk.StringVar(value="Matematicke priklady")
        title_entry = ttk.Entry(main_frame, textvariable=self.title_text, width=35)
        title_entry.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Seed (volitelny)
        ttk.Label(main_frame, text="Seed (volitelny):").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.seed = tk.StringVar(value="")
        seed_entry = ttk.Entry(main_frame, textvariable=self.seed, width=35)
        seed_entry.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Label(
            main_frame,
            text="(ponechte prazdne pro nahodne generovani)",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=row+1, column=1, sticky=tk.W, pady=(0, 10))
        row += 2

        # Vystupni soubor
        ttk.Label(main_frame, text="Vystupni soubor:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 15)
        )
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=(0, 15))

        self.output_file = tk.StringVar(value="priklady.xlsx")
        file_entry = ttk.Entry(file_frame, textvariable=self.output_file, width=25)
        file_entry.grid(row=0, column=0, sticky=tk.W)

        browse_button = ttk.Button(
            file_frame, text="Prochazet...", command=self.browse_file, width=12
        )
        browse_button.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        row += 1

        # Tlacitko Generovat
        generate_button = ttk.Button(
            main_frame,
            text="Generovat priklady",
            command=self.generate,
            width=30
        )
        generate_button.grid(row=row, column=0, columnspan=2, pady=(15, 0))

        # Konfigurace gridu pro roztahovani
        main_frame.columnconfigure(1, weight=1)

    def browse_file(self):
        """Otevre dialog pro vyber umisteni souboru."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel soubory", "*.xlsx"), ("Vsechny soubory", "*.*")],
            initialfile=self.output_file.get()
        )
        if filename:
            self.output_file.set(filename)

    def _get_selected_operations(self):
        """
        Vrati seznam vybranych operaci.

        Returns:
            List operacnich symbolu (+, -, *, /)
        """
        ops = []
        if self.op_add.get():
            ops.append("+")
        if self.op_sub.get():
            ops.append("-")
        if self.op_mul.get():
            ops.append("*")
        if self.op_div.get():
            ops.append("/")
        return ops

    def _validate_inputs(self, ops, max_result, count, cols, output_file):
        """
        Validuje vstupy od uzivatele.

        Returns:
            True pokud jsou vstupy validni, False jinak
        """
        if not ops:
            messagebox.showerror("Chyba", "Musite vybrat alespon jednu operaci!")
            return False

        if max_result < 1:
            messagebox.showerror("Chyba", "Maximalni vysledek musi byt alespon 1!")
            return False

        if count < 1:
            messagebox.showerror("Chyba", "Pocet prikladu musi byt alespon 1!")
            return False

        if cols < 1:
            messagebox.showerror("Chyba", "Pocet sloupcu musi byt alespon 1!")
            return False

        if not output_file:
            messagebox.showerror("Chyba", "Musite zadat vystupni soubor!")
            return False

        return True

    def generate(self):
        """Vygeneruje priklady podle zadanych parametru."""
        try:
            # Ziskani operaci
            ops = self._get_selected_operations()

            # Ziskani seed
            seed_value = None
            if self.seed.get().strip():
                try:
                    seed_value = int(self.seed.get().strip())
                except ValueError:
                    messagebox.showerror("Chyba", "Seed musi byt cele cislo!")
                    return

            # Ziskani ostatnich hodnot
            max_result = self.max_result.get()
            count = self.count.get()
            cols = self.cols.get()
            fill_mode = self.fill_mode.get()
            title = self.title_text.get()
            output_file = self.output_file.get()

            # Validace vstupu
            if not self._validate_inputs(ops, max_result, count, cols, output_file):
                return

            # Generovani souboru
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

            # Zobrazeni uspesne zpravy
            messagebox.showinfo(
                "Hotovo",
                f"Priklady byly uspesne vygenerovany!\n\nSoubor: {file_path}"
            )

            # Nabidka otevreni souboru
            if messagebox.askyesno("Otevrit soubor?", "Chcete soubor otevrit?"):
                self.open_file(file_path)

        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba pri generovani:\n{str(e)}")

    def open_file(self, file_path):
        """
        Otevre vygenerovany soubor v defaultni aplikaci.

        Args:
            file_path: Cesta k souboru k otevreni
        """
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS a Linux
                if os.uname().sysname == 'Darwin':  # macOS
                    subprocess.call(['open', file_path])
                else:  # Linux
                    subprocess.call(['xdg-open', file_path])
        except Exception as e:
            messagebox.showwarning(
                "Upozorneni",
                f"Nepodarilo se otevrit soubor:\n{str(e)}\n\nSoubor najdete v: {file_path}"
            )


def main():
    """Hlavni entry point pro GUI aplikaci."""
    root = tk.Tk()
    app = MathGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
