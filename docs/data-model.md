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

## Versione dei confini comunali

I comuni cambiano (fusioni, scorpori, modifiche di codice). Ogni riga di `territory_municipalities.csv` riporta quindi un `boundary_version`, che rimanda a `data/boundary_versions.csv`: per ciascuna versione si registrano la data di riferimento dei confini e dei codici ISTAT, l'URL della pubblicazione ISTAT e, quando possibile, il checksum del file usato. Così le geometrie possono essere ricostruite in futuro e l'elenco dei comuni può essere riallineato a una nuova versione senza perdere la storia. Nessuna versione è ancora registrata: la tabella resta vuota fino alla fase 3.

## Separazione fonte / risultato

`sources.csv` documenta cosa dice la fonte; `territory_municipalities.csv` è la rappresentazione operativa adottata. Se i comuni elencati dalla fonte differiscono da quelli adottati, la differenza si registra con `inclusion_status` (`boundary_case`, `excluded_after_review`) e con `notes`, collegando il record alla fonte tramite `source_id`. Un territorio senza fonte adeguata resta `unresolved` e senza comuni associati: non si assegnano comuni per analogia.

## Criteri di accettazione della fase 1

1. 70 record in `territories.csv`, senza `territory_id` né `name` duplicati.
2. Ogni `territory_id` è uno slug valido e coerente con `name` alla creazione; le dismissioni sono tracciate in `docs/id-migration.csv` e `CHANGELOG.md`.
3. `territory_type`, `macro_area` e `status` valorizzati; tutti i `status` sono `pending`.
4. Tabelle `territory_municipalities.csv`, `sources.csv` e `boundary_versions.csv` presenti con intestazioni e senza righe.
5. `python3 scripts/validate.py` termina senza problemi.

## Provenienza

Ogni delimitazione deve rimandare a uno o più record in `sources.csv`. Per fonti web, registrare l'URL stabile e la data di consultazione; per dataset scaricabili, registrare anche versione/data del dataset e, quando possibile, checksum.

## Valutazione delle fonti (fase 2)

`sources.csv` include `source_class` (`official`, `institutional`, `institutional_derivative`, `scholarly`, `encyclopedic`, `tourism`, `other`) e `lists_municipalities` (`yes`, `partial`, `no`). Una fonte è adeguata a popolare un territorio (fase 3) solo se appartiene a una classe `official`, `institutional` o `scholarly` e se `lists_municipalities` è `yes` o `partial`. Fonti enciclopediche o turistiche servono a documentare candidati e casi limite, non a definire il perimetro.

### `data/source_assessment.csv`

Valutazione preliminare per territorio, una riga per territorio valutato: `reference_unit` (unità amministrativa o fonte di riferimento), `match_type` (`exact`: coincide con l'unità; `unit_larger`: l'unità è più estesa del territorio; `multiple`: il territorio copre più unità; `unclear`), `outlook` (stato atteso, provvisorio, tra quelli di `status`) e `next_step`. Non modifica `status`: serve a pianificare la fase 3.
