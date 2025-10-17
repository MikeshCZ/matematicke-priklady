<a href="https://www.buymeacoffee.com/michalsara" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# Generátor matematických příkladů

Aplikace pro generování matematických příkladů do Excel souboru. Ideální pro učitele a rodiče, kteří potřebují rychle vytvořit cvičení pro děti.

## Funkce

- **Vícero operací**: Sčítání, odčítání, násobení, dělení
- **Nastavitelná obtížnost**: Maximální výsledek od 1 do 1000
- **Flexibilní rozvržení**: 1-10 sloupců, vyplňování po sloupcích nebo po řádcích
- **Reprodukovatelnost**: Volitelný seed pro vytvoření identických listů
- **Grafické rozhraní**: Intuitivní GUI aplikace
- **CLI rozhraní**: Pro pokročilé uživatele a automatizaci

## Instalace

```bash
# Klonování repozitáře
git clone https://github.com/uzivatel/matematicke-priklady.git
cd matematicke-priklady

# Instalace závislostí
pip install -r requirements.txt
```

## Použití

### GUI aplikace (doporučeno)

```bash
python src/main.py --gui
```

GUI nabízí:
- Výběr operací pomocí checkboxů
- Nastavení maximálního výsledku (1-1000)
- Počet příkladů (1-500)
- Počet sloupců (1-10)
- Způsob vyplňování (po sloupcích/řádcích)
- Vlastní titulek
- Volitelný seed pro reprodukovatelnost
- Procházení souborů pro výběr umístění

### CLI aplikace

```bash
# Nápověda - zobrazení všech dostupných argumentů
python src/main.py --help

# Základní použití (výchozí nastavení)
python src/main.py

# Pouze sčítání a odčítání, max výsledek 10
python src/main.py --ops "+-" --max 10

# 50 příkladů s násobením, 2 sloupce
python src/main.py --ops "*" --count 50 --cols 2

# S vlastním titulkem a seedem
python src/main.py --title "Cvičení 1" --seed 42

# Vyplňování po řádcích
python src/main.py --fill across

# Vlastní výstupní soubor
python src/main.py --out moje_priklady.xlsx
```

### Parametry CLI

| Parametr | Popis | Výchozí hodnota |
|----------|-------|-----------------|
| `-h`, `--help` | Zobrazení nápovědy a ukončení programu | - |
| `--ops OPERACE` | Operace k použití: '+' (sčítání), '-' (odčítání), '*' (násobení), '/' (dělení) | `"+-*/"` |
| `--max CISLO` | Maximální výsledek příkladu (1-1000) | `20` |
| `--count CISLO` | Počet příkladů k vygenerování (1-500) | `90` |
| `--cols CISLO` | Počet sloupců v rozvržení (1-10) | `3` |
| `--fill REZIM` | Způsob vyplňování: `down` (po sloupcích) nebo `across` (po řádcích) | `"down"` |
| `--title TEXT` | Titulek zobrazený v hlavičce listu | `"Matematické příklady"` |
| `--seed CISLO` | Seed pro reprodukovatelné generování (stejné číslo = stejné příklady) | náhodný |
| `--out SOUBOR` | Název výstupního .xlsx souboru | `"priklady.xlsx"` |

## Buildování aplikace

### macOS

Pro vytvoření standalone .app bundle:

```bash
./build_scripts/build_mac.sh
```

Výsledná aplikace bude v adresáři `dist/`. Build script:
- Automaticky zkontroluje a nainstaluje PyInstaller
- Vytvoří GUI aplikaci bez terminálového okna
- Použije konfiguraci z `gui.spec`

### Požadavky pro build
- PyInstaller (`pip install pyinstaller`)
- Všechny závislosti z `requirements.txt`

## Příklady výstupu

Aplikace generuje profesionálně naformátované Excel soubory s:
- Čitelným fontem Consolas (velikost 16, monospace)
- Jednotnou šířkou sloupců (cca 200px)
- Optimální výškou řádků (24)
- Volitelným titulkem (velikost 18, tučně)
- **Zarovnanými příklady** - všechny "=" jsou v každém sloupci pod sebou
- Úzkými okraji (0.25" po stranách, 0.75" nahoře/dole) pro optimální tisk

Formát příkladu: `a op b = ___`

Příklad (zarovnané):
```
  5 + 3 = ___
 12 - 7 = ___
  4 * 6 = ___
 15 / 3 = ___
```

## Požadavky

- Python 3.x
- openpyxl (pro generování Excel souborů)
- tkinter (zabudováno v Pythonu, pro GUI)

## Architektura projektu

Projekt se skládá ze tří hlavních modulů:

- **`src/main.py`** - Vstupní bod aplikace, směruje na CLI nebo GUI podle parametru `--gui`
- **`src/cli.py`** - Obsahuje veškerou jádrovou logiku:
  - Generátory příkladů (`gen_add`, `gen_sub`, `gen_mul`, `gen_div`)
  - Funkci `generate_sheet()` pro vytváření Excel souborů
  - CLI rozhraní pomocí argparse
- **`src/gui.py`** - GUI wrapper postavený na tkinter, který využívá `generate_sheet()` z `cli.py`

### Hlavní vlastnosti implementace

- **Zarovnávací algoritmus**: Příklady v každém sloupci jsou zarovnány doprava přidáním mezer, aby všechny znaky "=" byly pod sebou (využívá monospace font Consolas)
- **Matematická validita**:
  - Odčítání: vždy `a >= b` pro nezáporné výsledky
  - Dělení: výsledek vždy celé číslo (konstrukce `a = b * c`)
  - Sčítání/násobení: respektuje `max_result`
- **Strategie násobení**: Kandidátní přístup pro rovnoměrné rozložení operandů
- **Režimy vyplňování**:
  - `down` - po sloupcích (svisle)
  - `across` - po řádcích (vodorovně)

## Licence

Tento projekt je licencován pod GNU3 licencí - viz soubor [LICENSE](LICENSE).

## 🧑‍💻 Autor

- [Více o autorovi](https://www.michalsara.cz)

## ☕ Pokud se vám tato repository líbí, můžete **[mi koupit kafe](https://www.buymeacoffee.com/michalsara)**. Díky!
