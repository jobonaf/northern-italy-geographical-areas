#!/usr/bin/env python3
"""Controlli di coerenza sulle tabelle in data/. Uso: python3 scripts/validate.py"""
import csv, re, sys, unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
STATUS = {"pending", "defined_official", "defined_source", "defined_approximate", "unresolved"}
INCL = {"included", "boundary_case", "excluded_after_review"}
err = []

def read(n):
    with open(D / n, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

T = read("territories.csv")
ids = [r["territory_id"] for r in T]
names = [r["name"] for r in T]
for label, vals in (("territory_id", ids), ("name", names)):
    dup = {v for v in vals if vals.count(v) > 1}
    if dup: err.append(f"{label} duplicati: {sorted(dup)}")
for r in T:
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", r["territory_id"]): err.append(f"id non valido: {r['territory_id']}")
    if r["status"] not in STATUS: err.append(f"{r['territory_id']}: status non valido '{r['status']}'")
    for c in ("name", "territory_type", "macro_area"):
        if not r[c].strip(): err.append(f"{r['territory_id']}: {c} vuoto")
    if r["status"].startswith("defined") and not r["boundary_method"]: err.append(f"{r['territory_id']}: defined_* senza boundary_method")

S = {r["source_id"] for r in read("sources.csv")}
B = {r["boundary_version"] for r in read("boundary_versions.csv")}
seen = set()
for r in read("territory_municipalities.csv"):
    if r["territory_id"] not in ids: err.append(f"comune con territory_id sconosciuto: {r['territory_id']}")
    if r["inclusion_status"] not in INCL: err.append(f"inclusion_status non valido: {r['inclusion_status']}")
    if not re.fullmatch(r"\d{6}", r["istat_code"]): err.append(f"codice ISTAT non valido: {r['istat_code']}")
    if r["boundary_version"] not in B: err.append(f"boundary_version non registrata: {r['boundary_version']}")
    if r["source_id"] not in S: err.append(f"source_id sconosciuto: {r['source_id']}")
    k = (r["territory_id"], r["istat_code"])
    if k in seen: err.append(f"associazione duplicata: {k}")
    seen.add(k)
for r in read("sources.csv"):
    if r["territory_id"] not in ids: err.append(f"fonte con territory_id sconosciuto: {r['territory_id']}")

M = {"exact", "unit_larger", "multiple", "unclear"}
for r in read("source_assessment.csv"):
    if r["territory_id"] not in ids: err.append(f"valutazione con territory_id sconosciuto: {r['territory_id']}")
    if r["match_type"] not in M: err.append(f"match_type non valido: {r['match_type']}")
    if r["outlook"] not in STATUS - {"pending"}: err.append(f"outlook non valido: {r['outlook']}")

print(f"{len(T)} territori; {len(err)} problemi")
for e in err: print(" -", e)
sys.exit(1 if err else 0)
