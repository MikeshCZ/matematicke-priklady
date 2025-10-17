#!/usr/bin/env python3
import random
import argparse
import math
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter


# ----------------------------
# Generování příkladů
# ----------------------------
def gen_add(max_result):
    a = random.randint(0, max_result)
    b = random.randint(0, max_result - a)
    return a, "+", b, a + b


def gen_sub(max_result):
    a = random.randint(0, max_result)
    b = random.randint(0, a)
    return a, "-", b, a - b


def gen_mul(max_result):
    candidates = []
    for a in range(0, max_result + 1):
        if a == 0:
            candidates.append((0, "*", 0, 0))
            continue
        max_b = max_result // a
        b = random.randint(0, max_b)
        candidates.append((a, "*", b, a * b))
    return random.choice(candidates)


def gen_div(max_result):
    if max_result <= 0:
        return 0, "/", 1, 0
    c = random.randint(0, max_result)
    b = random.randint(1, max(1, max_result))
    a = b * c
    return a, "/", b, c


GEN_MAP = {
    "+": gen_add,
    "-": gen_sub,
    "*": gen_mul,
    "x": gen_mul,
    "/": gen_div,
    "÷": gen_div,
}


def make_problem_text(max_result, ops):
    op_key = random.choice(ops)
    a, op_sym, b, _ = GEN_MAP[op_key](max_result)
    return f"{a} {op_sym} {b} = ___"


# ----------------------------
# Užitečné
# ----------------------------
def auto_width(ws, col, min_width=12, pad=2):
    letter = get_column_letter(col)
    max_len = min_width
    for cell in ws[letter]:
        if cell.value is None:
            continue
        s = str(cell.value)
        max_len = max(max_len, len(s) + pad)
    ws.column_dimensions[letter].width = max_len


# ----------------------------
# Generování listu
# ----------------------------
def generate_sheet(
    ops, max_result, count, file_name, seed=None, title=None, cols=2, fill_mode="down"
):
    if seed is not None:
        random.seed(seed)

    ops = [o for o in ops if o in GEN_MAP]
    if not ops:
        raise ValueError("Žádná platná operace (+ - * /).")

    if cols < 1:
        cols = 1

    wb = Workbook()
    ws = wb.active
    ws.title = "Příklady"

    font = Font(name="Calibri", size=16)
    align_left = Alignment(horizontal="left", vertical="center")

    # Hlavička / titulek
    start_row = 1
    if title:
        ws.cell(row=start_row, column=1).value = title
        ws.cell(row=start_row, column=1).font = Font(name="Calibri", size=18, bold=True)
        start_row += 2

    # Připravíme si všechna cvičení dopředu
    problems = [make_problem_text(max_result, ops) for _ in range(count)]

    # Rozmístění do mřížky podle fill_mode
    # "down": sloupce se plní shora dolů (vhodné pro tisk)
    # "across": řádky se plní zleva doprava
    if fill_mode not in ("down", "across"):
        fill_mode = "down"

    rows_needed = math.ceil(count / cols)

    # Zapsat data
    idx = 0
    if fill_mode == "down":
        # Column-major: postupně sloupec 1, 2, ...
        for c in range(cols):
            for r in range(rows_needed):
                if idx >= count:
                    break
                cell = ws.cell(row=start_row + r, column=1 + c)
                cell.value = problems[idx]
                cell.font = font
                cell.alignment = align_left
                idx += 1
    else:  # across
        # Row-major: po řádcích
        for r in range(rows_needed):
            for c in range(cols):
                if idx >= count:
                    break
                cell = ws.cell(row=start_row + r, column=1 + c)
                cell.value = problems[idx]
                cell.font = font
                cell.alignment = align_left
                idx += 1

    # Nastavení pevné šířky sloupců (≈ 200 px)
    excel_width = 29  # cca 200 px
    for c in range(1, cols + 1):
        ws.column_dimensions[get_column_letter(c)].width = excel_width

    # Lehce zvýšíme řádkování kvůli čitelnosti
    last_row = start_row + rows_needed - 1
    for r in range(start_row, last_row + 1):
        ws.row_dimensions[r].height = 24

    wb.save(file_name)
    return file_name


# ----------------------------
# CLI
# ----------------------------
def parse_args():
    p = argparse.ArgumentParser(
        description="Generátor příkladů do Excelu (řádkový zápis, více sloupců)."
    )
    p.add_argument(
        "--ops",
        type=str,
        default="+-*/",
        help="Operace k použití (např. '+-' nebo '+-*/').",
    )
    p.add_argument("--max", type=int, default=20, help="Maximální výsledek.")
    p.add_argument("--count", type=int, default=78, help="Počet příkladů.")
    p.add_argument(
        "--seed", type=int, default=None, help="Seed pro reprodukovatelnost."
    )
    p.add_argument(
        "--out", type=str, default="priklady.xlsx", help="Výstupní .xlsx soubor."
    )
    p.add_argument(
        "--title", type=str, default="Matematické příklady", help="Titulek listu."
    )
    p.add_argument("--cols", type=int, default=3, help="Počet sloupců v Excelu.")
    p.add_argument(
        "--fill",
        type=str,
        default="down",
        choices=["down", "across"],
        help="Způsob vyplňování: 'down' (po sloupcích) nebo 'across' (po řádcích).",
    )
    return p.parse_args()


def main():
    args = parse_args()
    file_path = generate_sheet(
        ops=list(args.ops),
        max_result=args.max,
        count=args.count,
        file_name=args.out,
        seed=args.seed,
        title=args.title,
        cols=args.cols,
        fill_mode=args.fill,
    )
    print(f"Hotovo: {file_path}")


if __name__ == "__main__":
    main()
