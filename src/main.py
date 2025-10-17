#!/usr/bin/env python3
"""
Jednotný vstupní bod pro generátor matematických příkladů.

Bez argumentů nebo s běžnými CLI argumenty spouští CLI rozhraní.
S argumentem --gui spouští grafické rozhraní.
"""

import sys
import argparse

__version__ = "1.0.0"

def main():
    """Hlavní vstupní funkce."""
    # Kontrola, zda uživatel chce spustit GUI
    if '--gui' in sys.argv:
        # Odstranit --gui z argumentů před importem gui
        sys.argv.remove('--gui')

        # Importovat a spustit GUI
        from gui import main as gui_main
        gui_main()
    else:
        # Importovat a spustit CLI
        from cli import main as cli_main
        cli_main()


if __name__ == "__main__":
    main()
