<a href="https://www.buymeacoffee.com/michalsara" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# Generátor matematických příkladů

Aplikace pro generování matematických příkladů do Excel souboru. Ideální pro učitele a rodiče, kteří potřebují rychle vytvořit cvičení pro děti.

## Funkce

- **Vícero operací**: Sčítání, odčítání, násobení, dělení
- **Pokročilá kontrola obtížnosti**:
  - Maximální počet číslic v číslech (1-5 číslic)
  - Maximální hodnota výsledku (1-10000)
  - Možnost kombinovat oba parametry pro přesnou kontrolu
  - Možnost vyloučit nulu z příkladů
  - Možnost vyloučit jedničku z násobení a dělení (zabránění triviálním příkladům typu 5 × 1)
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
- Výběr operací pomocí checkboxů (+, -, ×, ÷)
- **Maximální počet číslic** (1-5) - omezuje velikost čísel v příkladech
- **Maximální výsledek** (0-10000) - omezuje maximální hodnotu výsledku (0 = neomezeno)
- **Bez nuly** - checkbox pro vyloučení čísla 0 z příkladů
- **Bez jedničky** - checkbox pro vyloučení čísla 1 z násobení a dělení
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

# Základní použití (výchozí nastavení: 2 číslice, 90 příkladů, 3 sloupce)
python src/main.py

# Příklady s 1 číslicí (čísla 0-9)
python src/main.py --digits 1

# Pouze sčítání a odčítání, max výsledek 20
python src/main.py --ops "+-" --max 20

# 50 příkladů s násobením, 2 sloupce
python src/main.py --ops "*" --count 50 --cols 2

# Čísla max 2 číslice, ale výsledek max 20
python src/main.py --digits 2 --max 20

# Bez nuly (vyloučit 0 z příkladů)
python src/main.py --no-zero

# Příklady s 1 číslicí, bez nuly (čísla 1-9)
python src/main.py --digits 1 --no-zero

# Bez jedničky (vyloučit 1 z násobení a dělení)
python src/main.py --no-one

# Bez nuly a jedničky pro násobení (čísla 2-99)
python src/main.py --ops "*" --no-zero --no-one

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
| `--digits CISLO` | **Maximální počet číslic** v číslech příkladu (1-5). Lze kombinovat s `--max` | `2` |
| `--max CISLO` | **Maximální výsledek** příkladu (1-10000). Lze kombinovat s `--digits` | není omezeno |
| `--no-zero` | **Vyloučit nulu** z příkladů (čísla budou pouze 1 a výše) | vypnuto |
| `--no-one` | **Vyloučit jedničku** z násobení a dělení (zabrání triviálním příkladům jako 5 × 1 nebo 6 ÷ 1) | vypnuto |
| `--count CISLO` | Počet příkladů k vygenerování (1-500) | `90` |
| `--cols CISLO` | Počet sloupců v rozvržení (1-10) | `3` |
| `--fill REZIM` | Způsob vyplňování: `down` (po sloupcích) nebo `across` (po řádcích) | `"down"` |
| `--title TEXT` | Titulek zobrazený v hlavičce listu | `"Matematické příklady"` |
| `--seed CISLO` | Seed pro reprodukovatelné generování (stejné číslo = stejné příklady) | náhodný |
| `--out SOUBOR` | Název výstupního .xlsx souboru | `"priklady.xlsx"` |

#### Jak fungují `--digits` a `--max` společně

- **`--digits`** omezuje **velikost jednotlivých čísel** v příkladu (např. `--digits 2` = čísla 0-99)
- **`--max`** omezuje **maximální hodnotu výsledku** operace
- Když jsou zadány oba parametry, platí **přísnější limit** pro každou část příkladu
- **Všechna čísla** v příkladech (včetně dělence) respektují oba limity

**Příklady kombinací:**
- `--digits 1` → čísla 0-9
- `--digits 2 --max 20` → čísla 0-99, ale výsledky ≤ 20
- `--digits 3 --max 50` → čísla 0-999, ale všechna čísla v příkladu ≤ 50
- `--max 100` → čísla omezena výsledkem 100

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
  - Odčítání s `--no-zero`: zajištěn nenulový výsledek (`a >= b + 1`)
  - Dělení: výsledek vždy celé číslo (konstrukce `a = b * c`)
  - Sčítání/násobení/dělení: respektuje `max_result` a `max_digits`
  - Všechna čísla respektují oba limity (`max_digits` a `max_result`)
- **Strategie násobení**: Kandidátní přístup pro rovnoměrné rozložení operandů
- **Pokročilá kontrola obtížnosti**:
  - `max_digits` omezuje počet číslic v jednotlivých číslech
  - `max_result` omezuje maximální hodnotu výsledku
  - Oba parametry lze kombinovat pro přesnou kontrolu
  - `no_zero` vyloučí nulu ze všech čísel v příkladech
  - `no_one` vyloučí jedničku z násobení a dělení (zabránění triviálním příkladům)
- **Režimy vyplňování**:
  - `down` - po sloupcích (svisle)
  - `across` - po řádcích (vodorovně)

## Licence

Tento projekt je licencován pod GNU3 licencí - viz soubor [LICENSE](LICENSE).

## 🧑‍💻 Autor

- [Více o autorovi](https://www.michalsara.cz)

## ☕ Pokud se vám tato repository líbí, můžete **[mi koupit kafe](https://www.buymeacoffee.com/michalsara)**. Díky!
