# Modello dati

## Identificativi

`territory_id` usa il formato `ITN-NNN`. Gli identificativi sono stabili e non dipendono dal nome o dalla regione amministrativa. Se un nome cambia, l'ID resta invariato; se due record vengono unificati, l'ID dismesso va documentato nel changelog.

## Stati di delimitazione

- `pending`: non ancora valutato.
- `defined_official`: delimitazione esplicita adottata da un ente competente.
- `defined_source`: delimitazione ricostruita da una fonte autorevole.
- `defined_approximate`: delimitazione operativa con margini interpretativi documentati.
- `unresolved`: non è stata individuata una fonte accettabile.

## Inclusione comunale

`inclusion_status` potrà assumere valori come `included`, `boundary_case` o `excluded_after_review`. Le esclusioni non vanno inserite come normali associazioni nel dataset finale, ma possono essere conservate durante la revisione se utili a documentare casi controversi.

## Provenienza

Ogni delimitazione deve rimandare a uno o più record in `sources.csv`. Per fonti web, registrare l'URL stabile e la data di consultazione; per dataset scaricabili, registrare anche versione/data del dataset e, quando possibile, checksum.
