# Generator matematickych prikladu

Aplikace pro generovani matematickych prikladu do Excel souboru. Idealni pro ucitele a rodice, kteri potrebuji rychle vytvorit cviceni pro deti.

## Funkce

- **Vicero operaci**: Scitani, odcitani, nasobeni, deleni
- **Nastavitelna obtiznost**: Maximalni vysledek od 1 do 1000
- **Flexibilni rozlozeni**: 1-10 sloupcu, vyplnovani po sloupcich nebo po radcich
- **Reprodukovatelnost**: Volitelny seed pro vytvoreni identickych listu
- **Graficke rozhrani**: Intuitivni GUI aplikace
- **CLI rozhrani**: Pro pokrocile uzivatele a automatizaci

## Instalace

```bash
# Klonovani repozitare
git clone https://github.com/uzivatel/matematicke-priklady.git
cd matematicke-priklady

# Instalace zavislosti
pip install -r requirements.txt
```

## Pouziti

### GUI aplikace (doporuceno)

```bash
python src/gui.py
```

GUI nabizi:
- Vyber operaci pomoci checkboxu
- Nastaveni maximalniho vysledku (1-1000)
- Pocet prikladu (1-500)
- Pocet sloupcu (1-10)
- Zpusob vyplnovani (po sloupcich/radcich)
- Vlastni titulek
- Volitelny seed pro reprodukovatelnost
- Prochazeni souboru pro vyber umisteni

### CLI aplikace

```bash
# Napoveda - zobrazeni vsech dostupnych argumentu
python src/main.py --help

# Zakladni pouziti (vychozi nastaveni)
python src/main.py

# Pouze scitani a odcitani, max vysledek 10
python src/main.py --ops "+-" --max 10

# 50 prikladu s nasobenim, 2 sloupce
python src/main.py --ops "*" --count 50 --cols 2

# S vlastnim titulkem a seedem
python src/main.py --title "Cviceni 1" --seed 42

# Vyplnovani po radcich
python src/main.py --fill across

# Vlastni vystupni soubor
python src/main.py --out moje_priklady.xlsx
```

### Parametry CLI

| Parametr | Popis | Vychozi hodnota |
|----------|-------|-----------------|
| `-h`, `--help` | Zobrazeni napovedy a ukonceni programu | - |
| `--ops OPERACE` | Operace k pouziti: '+' (scitani), '-' (odcitani), '*' (nasobeni), '/' (deleni) | `"+-*/"` |
| `--max CISLO` | Maximalni vysledek prikladu (1-1000) | `20` |
| `--count CISLO` | Pocet prikladu k vygenerovani (1-500) | `78` |
| `--cols CISLO` | Pocet sloupcu v rozlozeni (1-10) | `3` |
| `--fill REZIM` | Zpusob vyplnovani: `down` (po sloupcich) nebo `across` (po radcich) | `"down"` |
| `--title TEXT` | Titulek zobrazeny v hlavicce listu | `"Matematicke priklady"` |
| `--seed CISLO` | Seed pro reprodukovatelne generovani (stejne cislo = stejne priklady) | nahodny |
| `--out SOUBOR` | Nazev vystupniho .xlsx souboru | `"priklady.xlsx"` |

## Priklady vystupu

Aplikace generuje profesionalne naformatovane Excel soubory s:
- Citelnym fontem Calibri (velikost 16)
- Jednotnou sirkou sloupcu (cca 200px)
- Optimalni vyskou radku (24)
- Volitelnym titulkem (velikost 18, tucne)

Format prikladu: `a op b = ___`

Priklad:
```
5 + 3 = ___
12 - 7 = ___
4 * 6 = ___
15 / 3 = ___
```

## Pozadavky

- Python 3.x
- openpyxl (pro generovani Excel souboru)
- tkinter (zabudovano v Python, pro GUI)
