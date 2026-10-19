#!/usr/bin/env python3
"""Crea una mappa HTML interattiva dei territori definiti tramite comuni."""
from __future__ import annotations

import argparse
import html
import json
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import geopandas as gpd
import pandas as pd


def norm_code(series: pd.Series) -> pd.Series:
    """Normalizza un campo codice comunale a sei cifre."""
    return (
        series.astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.replace(r"\D", "", regex=True)
        .str.zfill(6)
    )


def detect_istat_column(gdf: gpd.GeoDataFrame, requested: str | None) -> str:
    if requested:
        if requested not in gdf.columns:
            raise ValueError(f"Colonna ISTAT richiesta non trovata: {requested}")
        return requested

    preferred = [
        "PRO_COM_T", "PRO_COM", "COD_PROCOM", "COD_COM", "COMUNE", "ISTAT_CODE"
    ]
    upper = {c.upper(): c for c in gdf.columns}
    for candidate in preferred:
        if candidate in upper:
            return upper[candidate]

    candidates = []
    for col in gdf.columns:
        if col == gdf.geometry.name:
            continue
        values = norm_code(gdf[col].dropna())
        if len(values) and values.str.fullmatch(r"\d{6}").mean() > 0.95:
            candidates.append(col)
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError(
        "Impossibile identificare automaticamente la colonna ISTAT. "
        f"Colonne disponibili: {list(gdf.columns)}. Usa --istat-column NOME."
    )


def detect_name_column(gdf: gpd.GeoDataFrame) -> str | None:
    upper = {c.upper(): c for c in gdf.columns}
    for candidate in ("COMUNE", "COMUNE_A", "DEN_COM", "DENOMINAZIONE", "NOME_COM"):
        if candidate in upper:
            return upper[candidate]
    return None


PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
    "#3182bd", "#e6550d", "#31a354", "#756bb1", "#636363",
    "#6baed6", "#fd8d3c", "#74c476", "#9e9ac8", "#969696",
    "#08519c", "#a63603", "#006d2c", "#54278f", "#252525",
]


def add_base_layer(fmap, tiles: str) -> None:
    """Aggiunge uno sfondo senza API key oppure nessuno sfondo."""
    import folium

    key = tiles.strip().lower()
    if key in {"none", "no", "off", "nessuno"}:
        return
    if key in {"osm", "openstreetmap"}:
        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="&copy; OpenStreetMap contributors",
            name="OpenStreetMap",
            overlay=False,
            control=True,
        ).add_to(fmap)
        return
    if key in {"opentopomap", "topo"}:
        folium.TileLayer(
            tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            attr="Map data &copy; OpenStreetMap contributors, SRTM | Map style &copy; OpenTopoMap",
            name="OpenTopoMap",
            overlay=False,
            control=True,
        ).add_to(fmap)
        return
    raise ValueError("Sfondo non valido. Usa: osm, opentopomap oppure none.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--shapefile",
        type=Path,
        default=Path(r"C:\scratch\dati\geodata\ConfiniAmministrativi\Limiti01012026_g\Com01012026_g\Com01012026_g_WGS84.shp"),
    )
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parent.parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent.parent / "output" / "territories_map.html")
    parser.add_argument("--istat-column", default=None)
    parser.add_argument("--tiles", default="osm", choices=["osm", "opentopomap", "none"], help="Sfondo senza API key")
    parser.add_argument("--serve", action="store_true", help="Avvia un server HTTP locale e apre la mappa")
    parser.add_argument("--port", type=int, default=8765, help="Porta del server locale")
    args = parser.parse_args()

    territories_path = args.data_dir / "territories.csv"
    links_path = args.data_dir / "territory_municipalities.csv"
    for path in (args.shapefile, territories_path, links_path):
        if not path.exists():
            raise FileNotFoundError(path)

    territories = pd.read_csv(territories_path, dtype=str, keep_default_na=False)
    links = pd.read_csv(links_path, dtype=str, keep_default_na=False)
    links["istat_code"] = norm_code(links["istat_code"])

    defined = territories.loc[territories["status"].eq("defined"), ["territory_id", "name"]]
    links = links.merge(defined, on="territory_id", how="inner", validate="many_to_one")

    comuni = gpd.read_file(args.shapefile)
    if comuni.crs is None:
        raise ValueError("Lo shapefile non dichiara il sistema di riferimento.")
    istat_col = detect_istat_column(comuni, args.istat_column)
    name_col = detect_name_column(comuni)
    comuni["istat_code"] = norm_code(comuni[istat_col])

    # La mappa rappresenta esclusivamente i codici presenti nei CSV.
    shape_codes = set(comuni["istat_code"])
    links_for_map = links.copy()

    missing = sorted(set(links_for_map["istat_code"]) - shape_codes)
    if missing:
        raise ValueError(
            f"{len(missing)} codici ISTAT non trovati nello shapefile: " + ", ".join(missing[:30])
        )

    selected = comuni.merge(links_for_map, on="istat_code", how="inner", validate="many_to_many")
    selected = selected.to_crs(4326)

    # Tooltip per comune. Un comune puo appartenere a piu territori.
    if name_col:
        selected["comune_label"] = selected[name_col].astype(str)
    else:
        selected["comune_label"] = selected["istat_code"]
    selected["tooltip"] = (
        "<b>" + selected["comune_label"].map(html.escape) + "</b><br>"
        + "ISTAT: " + selected["istat_code"] + "<br>"
        + "Territorio: " + selected["name"].map(html.escape)
    )

    try:
        import folium
        from folium.plugins import Fullscreen, Search
    except ImportError as exc:
        raise RuntimeError("Manca folium. Installa con: py -m pip install folium geopandas") from exc

    bounds = selected.total_bounds
    fmap = folium.Map(tiles=None, control_scale=True, prefer_canvas=True)
    add_base_layer(fmap, args.tiles)
    fmap.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    Fullscreen(position="topright").add_to(fmap)

    all_group = folium.FeatureGroup(name="Tutti i comuni definiti", show=True)
    all_group.add_to(fmap)

    territory_ids = sorted(selected["territory_id"].unique())
    territory_colors = {
        territory_id: PALETTE[i % len(PALETTE)]
        for i, territory_id in enumerate(territory_ids)
    }

    for territory_id, part in selected.groupby("territory_id", sort=True):
        territory_name = part["name"].iloc[0]
        color = territory_colors[territory_id]
        feature = folium.FeatureGroup(name=f"{territory_name} ({len(part)} comuni)", show=False)
        geo = folium.GeoJson(
            data=json.loads(part.to_json()),
            style_function=lambda _feature, c=color: {
                "color": c, "weight": 1.4, "fillColor": c, "fillOpacity": 0.35
            },
            highlight_function=lambda _feature: {"weight": 3, "fillOpacity": 0.65},
            tooltip=folium.GeoJsonTooltip(fields=["comune_label", "istat_code", "name"], aliases=["Comune", "ISTAT", "Territorio"]),
            name=territory_name,
        )
        geo.add_to(feature)
        feature.add_to(fmap)

    # Layer complessivo trasparente, utile alla ricerca per comune.
    search_geo = folium.GeoJson(
        data=json.loads(selected.to_json()),
        style_function=lambda _feature: {"color": "#555", "weight": 0.6, "fillOpacity": 0.05},
        tooltip=folium.GeoJsonTooltip(fields=["comune_label", "istat_code", "name"], aliases=["Comune", "ISTAT", "Territorio"]),
        name="Ricerca comuni",
        show=True,
    ).add_to(all_group)
    Search(search_geo, search_label="comune_label", placeholder="Cerca comune", collapsed=False).add_to(fmap)
    folium.LayerControl(collapsed=False).add_to(fmap)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fmap.save(args.output)

    overlaps = links.groupby("istat_code")["territory_id"].nunique()
    print(f"Shapefile: {args.shapefile}")
    print(f"Colonna ISTAT: {istat_col}; colonna nome: {name_col or 'non trovata'}")
    print(f"Territori rappresentati: {links['territory_id'].nunique()}")
    print(f"Associazioni rappresentate: {len(links)}")
    print(f"Comuni unici: {links['istat_code'].nunique()}")
    print(f"Comuni in piu territori: {(overlaps > 1).sum()}")
    print(f"Mappa: {args.output.resolve()}")

    if args.serve:
        serve_dir = args.output.parent.resolve()

        class MapHandler(SimpleHTTPRequestHandler):
            def __init__(self, *handler_args, **handler_kwargs):
                super().__init__(*handler_args, directory=str(serve_dir), **handler_kwargs)

            def log_message(self, format, *message_args):
                pass

        try:
            server = ThreadingHTTPServer(("127.0.0.1", args.port), MapHandler)
        except OSError as exc:
            raise RuntimeError(f"Porta {args.port} non disponibile. Prova con --port 8766.") from exc

        url = f"http://127.0.0.1:{args.port}/{args.output.name}"
        print(f"Server locale: {url}")
        print("Premi Ctrl+C per chiudere.")
        webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer chiuso.")
        finally:
            server.server_close()
    elif args.tiles != "none":
        print("Per visualizzare le tessere senza blocco, riesegui con --serve.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        raise SystemExit(1)
