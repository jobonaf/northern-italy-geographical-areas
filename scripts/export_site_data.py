#!/usr/bin/env python3
"""Esporta i territori e le relative fonti per il sito Jekyll."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

from map_territories import detect_istat_column, norm_code

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SHP = Path(r"C:\scratch\dati\geodata\ConfiniAmministrativi\Limiti01012026_g\Com01012026_g\Com01012026_g_WGS84.shp")


def read_csv(path: Path, required: tuple[str, ...]) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Colonne mancanti in {path}: {missing}")
    return frame


def sources_by_territory(sources: pd.DataFrame) -> dict[str, list[dict[str, str]]]:
    """Restituisce le fonti, ordinate e prive dei campi vuoti, per territorio."""
    fields = ("source_id", "title", "url", "source_type", "access_date", "notes")
    sources = sources.sort_values(["territory_id", "source_id"], kind="stable")
    result: dict[str, list[dict[str, str]]] = {}
    for territory_id, rows in sources.groupby("territory_id", sort=False):
        result[territory_id] = [
            {field: row[field].strip() for field in fields if field in rows.columns and row[field].strip()}
            for _, row in rows.iterrows()
        ]
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapefile", type=Path, default=DEFAULT_SHP)
    ap.add_argument("--data-dir", type=Path, default=ROOT / "data")
    ap.add_argument("--output", type=Path, default=ROOT / "docs" / "_data" / "territori.json")
    ap.add_argument("--istat-column", default=None)
    ap.add_argument("--tol", type=float, default=200.0, help="Tolleranza di semplificazione in metri")
    args = ap.parse_args()

    territories = read_csv(
        args.data_dir / "territories.csv", ("territory_id", "name", "status", "notes")
    )
    links = read_csv(
        args.data_dir / "territory_municipalities.csv", ("territory_id", "istat_code")
    )
    sources = read_csv(
        args.data_dir / "sources.csv", ("source_id", "territory_id", "title", "url")
    )

    links["istat_code"] = norm_code(links["istat_code"])
    defined_ids = set(territories.loc[territories["status"].eq("defined"), "territory_id"])
    links = links[links["territory_id"].isin(defined_ids)]

    comuni = gpd.read_file(args.shapefile)
    col = detect_istat_column(comuni, args.istat_column)
    comuni["istat_code"] = norm_code(comuni[col])
    missing = sorted(set(links["istat_code"]) - set(comuni["istat_code"]))
    if missing:
        raise ValueError(f"{len(missing)} codici ISTAT non trovati nello shapefile: {missing[:20]}")

    sel = comuni[["istat_code", "geometry"]].merge(
        links[["territory_id", "istat_code"]], on="istat_code", how="inner"
    ).to_crs(32632)
    diss = sel.dissolve(by="territory_id")[["geometry"]]
    diss["geometry"] = diss.geometry.simplify(args.tol, preserve_topology=True)

    n_comuni = links.groupby("territory_id")["istat_code"].nunique()
    out = territories.merge(diss, left_on="territory_id", right_index=True, how="left")
    out["n_comuni"] = out["territory_id"].map(n_comuni).fillna(0).astype(int)
    out = out.sort_values(["name", "territory_id"], kind="stable").reset_index(drop=True)
    gdf = gpd.GeoDataFrame(out, geometry="geometry", crs=32632).to_crs(4326)

    no_geom_defined = gdf[gdf["status"].eq("defined") & gdf.geometry.isna()]
    if len(no_geom_defined):
        print("ATTENZIONE: definiti ma senza geometria:", list(no_geom_defined["territory_id"]))

    source_map = sources_by_territory(sources)
    feature_collection = json.loads(gdf.to_json(drop_id=True, na="null"))
    for feature in feature_collection["features"]:
        properties = feature["properties"]
        territory_sources = source_map.get(properties["territory_id"], [])
        properties["sources"] = territory_sources
        properties["n_sources"] = len(territory_sources)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(feature_collection, stream, ensure_ascii=False, separators=(",", ":"))
        stream.write("\n")

    print("Stati:", gdf["status"].value_counts().to_dict())
    print(f"Con geometria: {gdf.geometry.notna().sum()} su {len(gdf)}")
    print(f"Con almeno una fonte: {sum(bool(v) for v in source_map.values())} su {len(gdf)}")
    print(f"Scritto {args.output} ({args.output.stat().st_size / 1e6:.2f} MB)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        raise SystemExit(1)
