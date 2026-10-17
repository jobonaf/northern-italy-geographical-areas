# Modello dati

## Identificativi

`territory_id` è uno slug testuale ASCII derivato dal nome canonico al momento della creazione (per esempio `langhe`, `val-d-ossola`, `bisiacaria`). Si usa il minuscolo, si eliminano i segni diacritici e si separano le parole con trattini; apostrofi e punteggiatura non sono conservati. L'ID è stabile e non dipende dalla regione amministrativa. Se il nome visualizzato cambia, l'ID resta invariato. Se due record vengono unificati, l'ID dismesso va documentato nel changelog e non può essere riutilizzato. In caso di collisione si aggiunge un qualificatore testuale significativo, non un numero progressivo. La migrazione iniziale da `ITN-NNN` è documentata in `docs/id-migration.csv`.

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
