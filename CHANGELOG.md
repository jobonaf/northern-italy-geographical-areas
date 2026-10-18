# Changelog

## Non rilasciato

- Modello dati semplificato a tre tabelle: `territories.csv` (`territory_id`, `name`, `status`, `notes`), `sources.csv` e `territory_municipalities.csv`.
- `status` ridotto a `pending`, `defined`, `unresolved`.
- Eliminati `territory_type`, `macro_area`, `boundary_method`, `source_assessment.csv` e `boundary_versions.csv`; le piste di ricerca dei territori senza fonti sono in `notes`.
- `sources.csv` registra solo fonti con elenchi di comuni o strati GIS (38 su 72 catalogate); gli ID `S….` non vengono rinumerati.
- Identificativi `ITN-NNN` sostituiti da slug testuali; mappa in `docs/id-migration.csv`.
- `scripts/validate.py` riscritto sul nuovo modello.
