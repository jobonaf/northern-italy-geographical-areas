# Changelog

## Non rilasciato

### Aggiunto

- Fonti per tutti i 70 territori censiti; `sources.csv` contiene attualmente 87 record.
- Popolamento della fase 3 con 756 associazioni in `territory_municipalities.csv`.
- Delimitazione di 28 territori tramite perimetri SNAI, elenchi istituzionali o convenzioni secondarie esplicite.
- `scripts/map_territories.py` per generare una mappa HTML interattiva dei territori `defined` a partire dallo shapefile comunale ISTAT 2026.
- Layer attivabili per territorio, colori distinti, tooltip, ricerca per comune, schermo intero e visualizzazione delle sovrapposizioni.
- Sfondi `osm`, `opentopomap` e `none`, senza API key.
- Raccordo cartografico per fusioni successive alla data dello shapefile, inizialmente per Castegnero Nanto.

### Modificato

- Il progetto e passato dalla fase 1 alla fase 3: popolamento delle associazioni territorio-comune.
- `scripts/validate.py` restituisce anche il numero e la percentuale di territori `defined`, oltre ai conteggi `pending` e `unresolved`.
- `Valtellina` e stata rinominata `Alta Valtellina`, adottando il perimetro SNAI di cinque comuni.
- Per Val d'Ossola, Valli di Lanzo, Valcamonica, Val Trompia, Lomellina e Oltrepo Pavese sono stati adottati perimetri SNAI.
- Per Canavese, Cusio, Acquese, Valli valdesi e Colli Berici sono state adottate liste comunali esplicite da Wikipedia.
- Per Biellese e Marca Trevigiana sono stati adottati rispettivamente i perimetri delle province di Biella e Treviso.
- Aggiornate le liste per fusioni comunali recenti, incluse San Giovanni di Fassa, Lusiana Conco, Alto Sermenza, Cellio con Breia e Ville di Fiemme.
- Corretto il codice ISTAT di Malvicino da `006089` a `006090`.

### Modello dati

- Modello semplificato a tre tabelle: `territories.csv`, `sources.csv` e `territory_municipalities.csv`.
- Stati ridotti a `pending`, `defined` e `unresolved`.
- Eliminati `territory_type`, `macro_area`, `boundary_method`, `source_assessment.csv` e `boundary_versions.csv`; criteri e questioni aperte sono registrati in `notes`.
- Identificativi `ITN-NNN` sostituiti da slug testuali; la mappa di migrazione e in `docs/id-migration.csv`.
- Gli ID delle fonti `SNNNN` non vengono rinumerati.

### Da completare

- Popolamento delle liste comunali per i territori ancora `pending` ma definibili mediante comuni.
- Acquisizione dei layer ufficiali per territori basati su porzioni di comuni, aree protette, denominazioni vitivinicole o beni UNESCO.
- Valutazione puntuale dei casi ancora ambigui, inclusi Romagna e Appennino emiliano.
