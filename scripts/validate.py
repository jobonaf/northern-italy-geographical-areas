#!/usr/bin/env python3
"""Controlli di coerenza sulle tabelle in data/. Uso: python3 scripts/validate.py"""
import csv, re, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / "data"
STATUS = {"pending", "defined", "unresolved"}
SOURCE_TYPES = {"list", "gis", "both"}
err = []

def read(name, cols):
    with open(D / name, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != cols:
            err.append(f"{name}: intestazione {reader.fieldnames}, attese {cols}")
        return list(reader)

def dups(values):
    return sorted({v for v in values if values.count(v) > 1})

T = read("territories.csv", ["territory_id", "name", "status", "notes"])
S = read("sources.csv", ["source_id", "territory_id", "title", "url", "source_type", "access_date", "notes"])
M = read("territory_municipalities.csv", ["territory_id", "istat_code", "source_id", "notes"])

ids = [r["territory_id"] for r in T]
for label, vals in (("territory_id", ids), ("name", [r["name"] for r in T]), ("source_id", [r["source_id"] for r in S])):
    if dups(vals): err.append(f"{label} duplicati: {dups(vals)}")

with_municipalities = {r["territory_id"] for r in M}
for r in T:
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", r["territory_id"]): err.append(f"id non valido: {r['territory_id']}")
    if not r["name"].strip(): err.append(f"{r['territory_id']}: name vuoto")
    if r["status"] not in STATUS: err.append(f"{r['territory_id']}: status non valido '{r['status']}'")
    if r["status"] == "defined" and r["territory_id"] not in with_municipalities:
        err.append(f"{r['territory_id']}: defined senza comuni")

source_ids = {r["source_id"] for r in S}
for r in S:
    if not re.fullmatch(r"S\d{4}", r["source_id"]): err.append(f"source_id non valido: {r['source_id']}")
    if r["territory_id"] not in ids: err.append(f"{r['source_id']}: territory_id sconosciuto {r['territory_id']}")
    if r["source_type"] not in SOURCE_TYPES: err.append(f"{r['source_id']}: source_type non valido '{r['source_type']}'")
    if not re.fullmatch(r"https?://\S+", r["url"]): err.append(f"{r['source_id']}: url non valido")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["access_date"]): err.append(f"{r['source_id']}: access_date non valida")

seen = set()
for r in M:
    if r["territory_id"] not in ids: err.append(f"comune con territory_id sconosciuto: {r['territory_id']}")
    if not re.fullmatch(r"\d{6}", r["istat_code"]): err.append(f"codice ISTAT non valido: {r['istat_code']}")
    if r["source_id"] and r["source_id"] not in source_ids: err.append(f"source_id sconosciuto: {r['source_id']}")
    k = (r["territory_id"], r["istat_code"])
    if k in seen: err.append(f"associazione duplicata: {k}")
    seen.add(k)

print(f"{len(T)} territori, {len(S)} fonti, {len(M)} associazioni; {len(err)} problemi")
for e in err: print(" -", e)
sys.exit(1 if err else 0)
