# Changelog

## Non rilasciato — fase 1 (struttura e anagrafica)

- Identificativi `ITN-NNN` sostituiti da slug testuali stabili; mappa in `docs/id-migration.csv`. Nessun ID dismesso o riutilizzato.
- Aggiunti `data/boundary_versions.csv` e le colonne `boundary_version` e `source_id` in `territory_municipalities.csv`.
- Documentati nel modello dati: versione dei confini, separazione fonte/risultato, criteri di accettazione.
- Aggiunto `scripts/validate.py`.
- Corretto l'albero dei file nel README (`LICENSE`, `docs/id-migration.csv`).
