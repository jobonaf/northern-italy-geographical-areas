#!/usr/bin/env python3
"""Create territory polygons from municipality assignments and reassign municipalities spatially.

Workflow:
1. Dissolve a reference municipality shapefile by territory_id.
2. Compare the resulting territory polygons with another municipality shapefile.
3. Write territory_id, territory_name, ISTAT assignments to CSV.

The script never edits the repository data files.
"""
from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd


TERRITORY_FIELDS = ["territory_id", "name", "status", "notes"]
LINK_FIELDS = ["territory_id", "istat_code", "source_id", "notes"]


def normalize_code(value) -> str:
    """Return a six-character ISTAT municipality code."""
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits.zfill(6) if digits else ""


def find_column(columns, requested, candidates, label):
    if requested:
        if requested not in columns:
            raise ValueError(f"Colonna {label} '{requested}' non trovata. Disponibili: {list(columns)}")
        return requested
    for candidate in candidates:
        if candidate in columns:
            return candidate
    raise ValueError(f"Colonna {label} non riconosciuta. Disponibili: {list(columns)}")


def read_csv_checked(path: Path, expected_fields):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_fields:
            raise ValueError(f"{path}: intestazione {reader.fieldnames}, attesa {expected_fields}")
        return list(reader)


def repair_geometry(frame: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    frame = frame[frame.geometry.notna() & ~frame.geometry.is_empty].copy()
    invalid = ~frame.geometry.is_valid
    if invalid.any():
        try:
            frame.loc[invalid, frame.geometry.name] = frame.loc[invalid].geometry.make_valid()
        except AttributeError:
            frame.loc[invalid, frame.geometry.name] = frame.loc[invalid].buffer(0)
    return frame[frame.geometry.notna() & ~frame.geometry.is_empty].copy()


def read_vector_with_encoding(path, encoding=None):
    """Read a vector dataset, retrying common Italian DBF encodings."""
    encodings = [encoding] if encoding else [None, "UTF-8", "CP1252", "ISO-8859-1"]
    errors = []
    for candidate in encodings:
        try:
            kwargs = {"encoding": candidate} if candidate else {}
            return gpd.read_file(path, **kwargs), candidate or "auto"
        except UnicodeDecodeError as exc:
            errors.append(f"{candidate or 'auto'}: {exc}")
        except Exception as exc:
            # Retry only errors plausibly caused by DBF text decoding.
            message = str(exc).lower()
            if any(token in message for token in ("codec", "decode", "encoding", "utf-8")):
                errors.append(f"{candidate or 'auto'}: {exc}")
            else:
                raise
    raise UnicodeError(
        f"Impossibile decodificare gli attributi di {path}. Tentativi: " + " | ".join(errors)
    )


def load_municipalities(path, code_column=None, name_column=None, encoding=None):
    frame, used_encoding = read_vector_with_encoding(path, encoding)
    if frame.crs is None:
        raise ValueError(f"CRS assente in {path}")
    code_col = find_column(
        frame.columns, code_column,
        ("PRO_COM_T", "PRO_COM", "COD_PROCOM", "istat_code", "ISTAT", "CODICE"),
        "ISTAT",
    )
    name_col = None
    if name_column or any(c in frame.columns for c in ("COMUNE", "DEN_COM", "COMUNE_A", "name")):
        name_col = find_column(
            frame.columns, name_column,
            ("COMUNE", "DEN_COM", "COMUNE_A", "name"),
            "nome comune",
        )
    keep = [code_col, frame.geometry.name] + ([name_col] if name_col else [])
    frame = frame[keep].copy()
    frame["ISTAT"] = frame[code_col].map(normalize_code)
    if name_col:
        frame["municipality_name"] = frame[name_col].astype(str)
    else:
        frame["municipality_name"] = ""
    frame = frame[frame["ISTAT"].str.fullmatch(r"\d{6}", na=False)].copy()
    if frame["ISTAT"].duplicated().any():
        duplicates = sorted(frame.loc[frame["ISTAT"].duplicated(False), "ISTAT"].unique())
        raise ValueError(f"Codici ISTAT duplicati in {path}: {duplicates[:20]}")
    return repair_geometry(frame[["ISTAT", "municipality_name", frame.geometry.name]])


def build_territories(data_dir, municipality_shp, output_shp, code_column=None, name_column=None,
                      include_pending=False, encoding=None):
    territories = read_csv_checked(data_dir / "territories.csv", TERRITORY_FIELDS)
    links = read_csv_checked(data_dir / "territory_municipalities.csv", LINK_FIELDS)
    tdf = pd.DataFrame(territories)
    if not include_pending:
        tdf = tdf[tdf["status"] == "defined"].copy()
    allowed = set(tdf["territory_id"])

    ldf = pd.DataFrame(links)
    ldf = ldf[ldf["territory_id"].isin(allowed)].copy()
    ldf["ISTAT"] = ldf["istat_code"].map(normalize_code)
    municipalities = load_municipalities(municipality_shp, code_column, name_column, encoding)
    available = set(municipalities["ISTAT"])
    missing = sorted(set(ldf["ISTAT"]) - available)
    if missing:
        raise ValueError(
            f"{len(missing)} codici dei CSV non presenti nello shapefile di riferimento: "
            + ", ".join(missing[:30])
        )

    joined = municipalities.merge(ldf[["territory_id", "ISTAT"]], on="ISTAT", how="inner")
    joined = joined.merge(tdf[["territory_id", "name"]], on="territory_id", how="left")
    dissolved = joined[["territory_id", "name", "geometry"]].dissolve(
        by=["territory_id", "name"], as_index=False
    )
    dissolved = repair_geometry(dissolved)

    output_shp.parent.mkdir(parents=True, exist_ok=True)
    # Shapefile names are limited to 10 characters. Keep stable short names.
    shp = dissolved.rename(columns={"territory_id": "terr_id", "name": "terr_name"})
    shp.to_file(output_shp, driver="ESRI Shapefile", encoding="UTF-8")
    return dissolved


def assign_municipalities(territories, target_shp, output_csv, audit_csv, threshold,
                          territory_coverage_threshold, area_crs, original_pairs,
                          code_column=None, name_column=None, encoding=None,
                          rule="municipality_share"):
    targets = load_municipalities(target_shp, code_column, name_column, encoding)
    territories = repair_geometry(territories)

    targets_area = targets.to_crs(area_crs)
    territories_area = territories.to_crs(area_crs)
    targets_area["municipality_area"] = targets_area.geometry.area
    territories_area["territory_area"] = territories_area.geometry.area

    intersections = gpd.overlay(
        targets_area[["ISTAT", "municipality_name", "municipality_area", "geometry"]],
        territories_area[["territory_id", "name", "territory_area", "geometry"]],
        how="intersection",
        keep_geom_type=False,
    )
    intersections = intersections[
        intersections.geometry.notna() & ~intersections.geometry.is_empty
    ].copy()
    intersections["intersection_area"] = intersections.geometry.area
    intersections["municipality_share"] = (
        intersections["intersection_area"] / intersections["municipality_area"]
    ).clip(0, 1)
    intersections["territory_share"] = (
        intersections["intersection_area"] / intersections["territory_area"]
    ).clip(0, 1)

    if rule == "municipality_share":
        selected = intersections[intersections["municipality_share"] >= threshold].copy()
    elif rule == "either_share":
        selected = intersections[
            (intersections["municipality_share"] >= threshold)
            | (intersections["territory_share"] >= territory_coverage_threshold)
        ].copy()
    elif rule == "centroid":
        centroids = targets_area.copy()
        centroids.geometry = centroids.geometry.representative_point()
        selected_keys = gpd.sjoin(
            centroids[["ISTAT", "geometry"]],
            territories_area[["territory_id", "geometry"]],
            how="inner", predicate="within",
        )[["ISTAT", "territory_id"]].drop_duplicates()
        selected = intersections.merge(selected_keys, on=["ISTAT", "territory_id"], how="inner")
    else:
        raise ValueError(f"Regola non supportata: {rule}")

    selected = selected.sort_values(
        ["territory_id", "municipality_share", "ISTAT"], ascending=[True, False, True]
    )
    assignments = selected[["territory_id", "name", "ISTAT"]].drop_duplicates()
    assignments = assignments.rename(columns={"name": "territory_name"})
    assignments["assignment_status"] = [
        "existing" if (territory_id, istat) in original_pairs else "new"
        for territory_id, istat in zip(assignments["territory_id"], assignments["ISTAT"])
    ]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    assignments.to_csv(output_csv, index=False, encoding="utf-8", lineterminator="\n")

    audit = intersections[[
        "territory_id", "name", "ISTAT", "municipality_name",
        "municipality_share", "territory_share", "intersection_area"
    ]].copy()
    audit = audit.rename(columns={"name": "territory_name"})
    selected_keys = set(zip(assignments["territory_id"], assignments["ISTAT"]))
    audit["originally_assigned"] = [
        (tid, code) in original_pairs for tid, code in zip(audit["territory_id"], audit["ISTAT"])
    ]
    audit["selected"] = [
        (tid, code) in selected_keys for tid, code in zip(audit["territory_id"], audit["ISTAT"])
    ]
    audit["assignment_status"] = [
        "existing" if original and selected else
        "new" if (not original and selected) else
        "dropped" if (original and not selected) else
        "candidate_excluded"
        for original, selected in zip(audit["originally_assigned"], audit["selected"])
    ]
    audit = audit.sort_values(
        ["territory_id", "municipality_share", "ISTAT"], ascending=[True, False, True]
    )
    audit.to_csv(audit_csv, index=False, encoding="utf-8", lineterminator="\n", float_format="%.6f")
    return assignments, audit


def main():
    parser = argparse.ArgumentParser(
        description="Crea shapefile dei territori e riassegna comuni mediante sovrapposizione spaziale."
    )
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--reference-municipalities", required=True,
                        help="Shapefile usato per costruire i territori dai CSV correnti")
    parser.add_argument("--target-municipalities", required=True,
                        help="Altro shapefile comunale da classificare")
    parser.add_argument("--territories-shp", default="output/territories.shp")
    parser.add_argument("--output-csv", default="output/territory_assignment.csv")
    parser.add_argument("--audit-csv", default="output/territory_assignment_audit.csv")
    parser.add_argument("--reference-code-column")
    parser.add_argument("--reference-name-column")
    parser.add_argument("--target-code-column")
    parser.add_argument("--target-name-column")
    parser.add_argument("--reference-encoding", default=None,
                        help="Codifica DBF dello shapefile di riferimento, es. CP1252")
    parser.add_argument("--target-encoding", default=None,
                        help="Codifica DBF dello shapefile target, es. CP1252")
    parser.add_argument("--area-crs", default="EPSG:3035",
                        help="CRS metrico/equal-area usato per le percentuali (default EPSG:3035)")
    parser.add_argument("--threshold", type=float, default=0.50,
                        help="Quota minima dell'area del comune inclusa nel territorio, 0-1 (default 0.50)")
    parser.add_argument("--territory-coverage-threshold", type=float, default=0.05,
                        help="Quota minima del territorio coperta dal comune per --rule either_share")
    parser.add_argument("--rule", choices=("municipality_share", "either_share", "centroid"),
                        default="municipality_share")
    parser.add_argument("--include-pending", action="store_true")
    args = parser.parse_args()

    if not 0 <= args.threshold <= 1:
        parser.error("--threshold deve essere compreso tra 0 e 1")
    if not 0 <= args.territory_coverage_threshold <= 1:
        parser.error("--territory-coverage-threshold deve essere compreso tra 0 e 1")

    territories = build_territories(
        Path(args.data_dir), Path(args.reference_municipalities), Path(args.territories_shp),
        args.reference_code_column, args.reference_name_column, args.include_pending,
        args.reference_encoding,
    )
    original_links = read_csv_checked(Path(args.data_dir) / "territory_municipalities.csv", LINK_FIELDS)
    original_pairs = {
        (row["territory_id"], normalize_code(row["istat_code"]))
        for row in original_links
    }
    assignments, audit = assign_municipalities(
        territories, Path(args.target_municipalities), Path(args.output_csv), Path(args.audit_csv),
        args.threshold, args.territory_coverage_threshold, args.area_crs, original_pairs,
        args.target_code_column, args.target_name_column, args.target_encoding, args.rule,
    )
    print(f"Territori creati: {len(territories)} -> {args.territories_shp}")
    counts = assignments["assignment_status"].value_counts().to_dict()
    print(f"Assegnazioni: {len(assignments)} -> {args.output_csv}")
    print(f"  esistenti: {counts.get('existing', 0)}; nuove: {counts.get('new', 0)}")
    print(f"Audit intersezioni: {len(audit)} -> {args.audit_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"ERRORE: {exc}")
