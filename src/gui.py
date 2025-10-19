#!/usr/bin/env python3
"""
GUI aplikace pro generovani matematickych prikladu.
Poskytuje graficke rozhrani pro vsechny funkce generatoru.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
from cli import generate_sheet, __version__


class MathGeneratorGUI:
    """GUI aplikace pro generovani matematickych prikladu."""

    def __init__(self, root):
        """
        Inicializuje GUI aplikaci.

        Args:
            root: Korenovy tkinter widget
        """
        self.root = root
        self.root.title(f"Generátor matematických příkladů | v{__version__}")
        self.root.geometry("600x660")
        self.root.resizable(False, False)

        # Vycentrovani okna na obrazovce
        self._center_window()

        # Vytvoreni hlavniho framu s paddingem
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Titulek aplikace
        title_label = ttk.Label(
            main_frame,
            text="Generátor matematických příkladů",
            font=("Arial", 16, "bold"),
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

        ttk.Checkbutton(ops_frame, text="Sčítání (+)", variable=self.op_add).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 20)
        )
        ttk.Checkbutton(ops_frame, text="Odčítání (-)", variable=self.op_sub).grid(
            row=0, column=1, sticky=tk.W, padx=(0, 20)
        )
        ttk.Checkbutton(ops_frame, text="Násobení (×)", variable=self.op_mul).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(5, 0)
        )
        ttk.Checkbutton(ops_frame, text="Dělení (/)", variable=self.op_div).grid(
            row=1, column=1, sticky=tk.W, pady=(5, 0)
        )

        row += 2

        # Maximalni pocet cislic
        ttk.Label(main_frame, text="Maximální počet číslic:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.max_digits = tk.IntVar(value=2)
        digits_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=5, textvariable=self.max_digits, width=20
        )
        digits_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Label(
            main_frame,
            text="(např. 2 = čísla 0-99, 3 = čísla 0-999)",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=row+1, column=1, sticky=tk.W, pady=(0, 10))
        row += 2

        # Maximalni vysledek
        ttk.Label(main_frame, text="Maximální výsledek:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.max_result = tk.IntVar(value=0)  # 0 = neomezeno
        max_result_spinbox = ttk.Spinbox(
            main_frame, from_=0, to=10000, textvariable=self.max_result, width=20
        )
        max_result_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Label(
            main_frame,
            text="(0 = neomezeno, jinak max hodnota výsledku)",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=row+1, column=1, sticky=tk.W, pady=(0, 10))
        row += 2

        # Checkbox pro vylouceni nuly
        self.no_zero = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            main_frame,
            text="Bez nuly (vyloučit číslo 0 z příkladů)",
            variable=self.no_zero
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        row += 1

        # Pocet prikladu
        ttk.Label(main_frame, text="Počet příkladů:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.count = tk.IntVar(value=90)
        count_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=500, textvariable=self.count, width=20
        )
        count_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Pocet sloupcu
        ttk.Label(main_frame, text="Počet sloupců:").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.cols = tk.IntVar(value=3)
        cols_spinbox = ttk.Spinbox(
            main_frame, from_=1, to=10, textvariable=self.cols, width=20
        )
        cols_spinbox.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        row += 1

        # Zpusob vyplnovani
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

        # Seed (volitelny)
        ttk.Label(main_frame, text="Seed (volitelné):").grid(
            row=row, column=0, sticky=tk.W, pady=(0, 10)
        )
        self.seed = tk.StringVar(value="")
        seed_entry = ttk.Entry(main_frame, textvariable=self.seed, width=35)
        seed_entry.grid(row=row, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Label(
            main_frame,
            text="(ponechte prázdné pro náhodné generovaní)",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=row+1, column=1, sticky=tk.W, pady=(0, 10))
        row += 2

        # Vystupni soubor
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

        # Tlacitko Generovat
        generate_button = ttk.Button(
            main_frame,
            text="Generovat příklady",
            command=self.generate,
            width=30
        )
        generate_button.grid(row=row, column=0, columnspan=2, pady=(15, 0))

        # Konfigurace gridu pro roztahovani
        main_frame.columnconfigure(1, weight=1)

    def _center_window(self):
        """Vycentruje okno na stredu obrazovky."""
        self.root.update_idletasks()

        # Ziskani rozmeru okna
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Ziskani rozmeru obrazovky
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Vypocet pozice pro vycentrovani
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Nastaveni pozice okna
        self.root.geometry(f"+{x}+{y}")

    def browse_file(self):
        """Otevre dialog pro vyber umisteni souboru."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel soubory", "*.xlsx"), ("Všechny soubory", "*.*")],
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

    def _validate_inputs(self, ops, max_digits, count, cols, output_file):
        """
        Validuje vstupy od uzivatele.

        Returns:
            True pokud jsou vstupy validni, False jinak
        """
        if not ops:
            messagebox.showerror("Chyba", "Musíte vybrat alespoň jednu operaci!")
            return False

        if max_digits < 1:
            messagebox.showerror("Chyba", "Maximální počet číslic musí být alespoň 1!")
            return False

        if count < 1:
            messagebox.showerror("Chyba", "Počet příkladů musí být alespoň 1!")
            return False

        if cols < 1:
            messagebox.showerror("Chyba", "Počet sloupců musí být alespoň 1!")
            return False

        if not output_file:
            messagebox.showerror("Chyba", "Musíte zadat výstupní soubor!")
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
                    messagebox.showerror("Chyba", "Seed musí být celé číslo!")
                    return

            # Ziskani ostatnich hodnot
            max_digits = self.max_digits.get()
            max_result = self.max_result.get()
            # Pokud je max_result 0, bude None (neomezeno)
            max_result = max_result if max_result > 0 else None
            count = self.count.get()
            cols = self.cols.get()
            fill_mode = self.fill_mode.get()
            title = self.title_text.get()
            output_file = self.output_file.get()
            no_zero = self.no_zero.get()

            # Validace vstupu
            if not self._validate_inputs(ops, max_digits, count, cols, output_file):
                return

            # Generovani souboru
            file_path = generate_sheet(
                ops=ops,
                count=count,
                file_name=output_file,
                max_result=max_result,
                max_digits=max_digits,
                seed=seed_value,
                title=title if title else None,
                cols=cols,
                fill_mode=fill_mode,
                no_zero=no_zero
            )

            # Zobrazeni uspesne zpravy
            messagebox.showinfo(
                "Hotovo",
                f"Příklady byly úspěšně vygenerovány!\n\nSoubor: {file_path}"
            )

            # Nabidka otevreni souboru
            if messagebox.askyesno("Otevřít soubor?", "Chcete soubor otevřít?"):
                self.open_file(file_path)

        except Exception as e:
            messagebox.showerror("Chyba", f"Nastala chyba při generování:\n{str(e)}")

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
                "Upozornění",
                f"Nepodařilo se otevřít soubor:\n{str(e)}\n\nSoubor najdete v: {file_path}"
            )


def main():
    """Hlavni entry point pro GUI aplikaci."""
    root = tk.Tk()
    app = MathGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
