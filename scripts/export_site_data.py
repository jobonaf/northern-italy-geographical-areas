#!/usr/bin/env python3
"""Esporta i territori per il sito Jekyll: docs/_data/territori.json.

Unisce i comuni di ciascun territorio definito (data/territory_municipalities.csv)
in un unico poligono semplificato e aggiunge, senza geometria, i territori
non ancora definiti, cosi' il sito puo' elencarli come "da risolvere".
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

from map_territories import detect_istat_column, norm_code

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SHP = Path(r"C:\scratch\dati\geodata\ConfiniAmministrativi\Limiti01012026_g\Com01012026_g\Com01012026_g_WGS84.shp")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapefile", type=Path, default=DEFAULT_SHP)
    ap.add_argument("--data-dir", type=Path, default=ROOT / "data")
    ap.add_argument("--output", type=Path, default=ROOT / "docs" / "_data" / "territori.json")
    ap.add_argument("--istat-column", default=None)
    ap.add_argument("--tol", type=float, default=200.0, help="Tolleranza di semplificazione in metri")
    args = ap.parse_args()

    territories = pd.read_csv(args.data_dir / "territories.csv", dtype=str, keep_default_na=False)
    links = pd.read_csv(args.data_dir / "territory_municipalities.csv", dtype=str, keep_default_na=False)
    links["istat_code"] = norm_code(links["istat_code"])
    defined_ids = set(territories.loc[territories["status"].eq("defined"), "territory_id"])
    links = links[links["territory_id"].isin(defined_ids)]

    comuni = gpd.read_file(args.shapefile)
    col = detect_istat_column(comuni, args.istat_column)
    comuni["istat_code"] = norm_code(comuni[col])
    missing = sorted(set(links["istat_code"]) - set(comuni["istat_code"]))
    if missing:
        raise ValueError(f"{len(missing)} codici ISTAT non trovati nello shapefile: {missing[:20]}")

    # Si lavora in metri (UTM 32N) per unire e semplificare, poi si torna a WGS84.
    sel = comuni[["istat_code", "geometry"]].merge(
        links[["territory_id", "istat_code"]], on="istat_code", how="inner"
    ).to_crs(32632)
    diss = sel.dissolve(by="territory_id")[["geometry"]]
    diss["geometry"] = diss.geometry.simplify(args.tol, preserve_topology=True)

    n_comuni = links.groupby("territory_id")["istat_code"].nunique()
    out = territories.merge(diss, left_on="territory_id", right_index=True, how="left")
    out["n_comuni"] = out["territory_id"].map(n_comuni).fillna(0).astype(int)
    gdf = gpd.GeoDataFrame(out, geometry="geometry", crs=32632).to_crs(4326)

    no_geom_defined = gdf[gdf["status"].eq("defined") & gdf.geometry.isna()]
    if len(no_geom_defined):
        print("ATTENZIONE: definiti ma senza geometria:", list(no_geom_defined["territory_id"]))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(args.output, driver="GeoJSON")
    print("Stati:", gdf["status"].value_counts().to_dict())
    print(f"Con geometria: {gdf.geometry.notna().sum()} su {len(gdf)}")
    print(f"Scritto {args.output} ({args.output.stat().st_size / 1e6:.2f} MB)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        raise SystemExit(1)
