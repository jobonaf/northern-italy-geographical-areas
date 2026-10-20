# Changelog

## Non rilasciato

### Aggiunto

- Copertura portata a 76 territori e 93 fonti.
- Popolamento della fase 3 portato a 1.410 associazioni territorio-comune.
- Delimitazione di 62 territori mediante perimetri SNAI, elenchi istituzionali o convenzioni secondarie esplicite.
- Aggiunti Val Nure, Val Ceno, Val Trebbia, Colline Matildiche, Alta Valmarecchia, Romagna Toscana e Valle del Lamone.
- Definiti Langhe mediante Bassa Langa, Alta Langa, Langa Astigiana e Langa Monregalese, escludendo il Roero.
- Monferrato rinominato Alto Monferrato e definito mediante l'area regionale di 41 comuni.
- Definiti Cadore, Ampezzano, Agordino, Polesine, Val di Susa, Vergante, Valsassina, Valsugana e Valbelluna.
- `scripts/map_territories.py` genera una mappa HTML interattiva con layer per territorio, colori distinti, tooltip, ricerca per comune, schermo intero e visualizzazione delle sovrapposizioni.
- Aggiunte a `map_territories.py` le opzioni `--serve` e `--port` per servire la mappa tramite HTTP locale.
- Sfondi `osm`, `opentopomap` e `none`, senza API key.

### Modificato

- Il progetto e nella fase 3: popolamento e revisione delle associazioni territorio-comune.
- `scripts/validate.py` restituisce numero e percentuale dei territori `defined`, oltre ai conteggi `pending` e `unresolved`.
- La rappresentazione corrente usa esclusivamente aggregazioni di comuni interi; non vengono versionati layer o GeoJSON dedicati ai territori.
- Gli script di aggiunta, correzione e migrazione sono considerati strumenti temporanei di lavoro e non vengono inclusi nel repository.
- `map_territories.py` non applica raccordi o correzioni ad hoc: visualizza esclusivamente i codici presenti nei CSV.
- Val Pusteria ridotta a 17 comuni, escludendo Val Badia e Valli di Tures-Aurina.
- Valbelluna ampliata dalla precedente aggregazione amministrativa ristretta a un perimetro geografico operativo di 13 comuni, comprendente Belluno e Feltre.
- Val d'Adige eliminata dal repertorio.
- Valtellina rinominata Alta Valtellina, adottando il perimetro SNAI di cinque comuni.
- Per Val d'Ossola, Valli di Lanzo, Valcamonica, Val Trompia, Lomellina e Oltrepo Pavese sono stati adottati perimetri SNAI.
- Per Canavese, Cusio, Acquese, Valli valdesi e Colli Berici sono state adottate liste comunali esplicite.
- Per Biellese e Marca Trevigiana sono stati adottati rispettivamente i perimetri delle province di Biella e Treviso.
- Aggiornate le liste per fusioni comunali recenti, incluse San Giovanni di Fassa, Lusiana Conco, Alto Sermenza, Cellio con Breia, Ville di Fiemme, Borgomezzavalle, Treppo Ligosullo e Castegnero Nanto.

### Corretto

- Corretti numerosi abbinamenti tra nomi comunali e codici ISTAT individuati mediante ispezione cartografica.
- Aggiunti Ceto e Cevo alla Valcamonica; Nadro e rappresentato tramite il comune di Ceto.
- Rimosso Bondone dalla Vallagarina e ripristinato Brentonico.
- Corretti i perimetri di Carnia, Slavia friulana e Bisiacaria.
- Corretti i perimetri di Acquese, Cusio, Val di Sole, Val di Fassa, Vallagarina, Valli valdesi e Valsesia.
- Corretto il codice ISTAT di Malvicino da `006089` a `006090`.
- Corretto il codice di Sappada al valore corrente `030189`.
- Ripristinate le fonti sovrascritte di Canavese, Biellese e Val di Fassa.

### Modello dati

- Modello basato su tre tabelle: `territories.csv`, `sources.csv` e `territory_municipalities.csv`.
- Stati ammessi: `pending`, `defined` e `unresolved`.
- Gli identificativi territoriali sono slug testuali stabili; gli ID delle fonti `SNNNN` non vengono rinumerati.
- Le sovrapposizioni e le relazioni di inclusione tra territori sono ammesse.
- I territori non rappresentabili adeguatamente mediante comuni interi restano `pending`.

### Da completare

- Definizione dei 14 territori ancora `pending` mediante liste comunali documentate o scelta metodologica esplicita.
- Verifica cartografica dei nuovi perimetri e controllo sistematico della corrispondenza nome-codice ISTAT.
- Valutazione puntuale dei casi ancora ambigui, inclusi Romagna, Appennino emiliano, Brianza e Carso.
