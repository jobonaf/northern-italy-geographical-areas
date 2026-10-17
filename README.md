# Territori geografici del Nord Italia

Repertorio in costruzione di territori geografici riconoscibili del Nord Italia, pensato per analisi territoriali e uso GIS.

## Stato del progetto

Il repository si trova nella **fase 1: struttura e anagrafica**. I 70 record sono candidati iniziali; non rappresentano ancora delimitazioni validate. Nessun comune è assegnato automaticamente e nessun poligono è incluso in questa fase.

## Criteri

- I territori sono selezionati per riconoscibilità geografica, storica o culturale.
- Le delimitazioni possono sovrapporsi.
- Un territorio che attraversa più regioni amministrative mantiene un solo identificativo.
- I laghi come entità autonome e i territori liguri sono esclusi dal repertorio corrente.
- Non si inventano elenchi di comuni per colmare lacune documentali.
- Le fonti e i criteri di delimitazione saranno registrati separatamente dai dati derivati.

## Struttura

```text
.
├── README.md
├── CITATION.cff
├── LICENSE
├── .gitignore
├── data/
│   ├── territories.csv
│   ├── territory_municipalities.csv
│   ├── sources.csv
│   ├── source_assessment.csv
│   └── boundary_versions.csv
├── docs/
│   ├── data-model.md
│   └── id-migration.csv
├── scripts/
│   └── validate.py
└── CHANGELOG.md
```

## Tabelle

### `data/territories.csv`

Una riga per territorio. `territory_id` è uno slug testuale stabile (per esempio `langhe` o `val-d-ossola`): non codifica confini amministrativi e non va riutilizzato per un altro territorio. È derivato dal nome iniziale, ma non viene aggiornato automaticamente quando cambia `name`. La migrazione dagli ID numerici iniziali è documentata in `docs/id-migration.csv`.

- `territory_type`: classificazione descrittiva provvisoria.
- `macro_area`: raggruppamento editoriale per organizzare il lavoro, non una delimitazione amministrativa.
- `status`: stato della verifica della delimitazione (`pending`, `defined_official`, `defined_source`, `defined_approximate`, `unresolved`).
- `boundary_method`: metodo usato per definire il territorio, da compilare dopo la verifica.
- `notes`: osservazioni e questioni da verificare.

### `data/territory_municipalities.csv`

Tabella relazionale: una riga per ogni associazione territorio-comune. I codici ISTAT saranno aggiunti dopo aver consultato una versione documentata dei confini e dei codici comunali.

### `data/boundary_versions.csv`

Registro delle versioni dei confini e dei codici comunali ISTAT (data di riferimento, URL, checksum). Ogni riga di `territory_municipalities.csv` rimanda a una versione tramite `boundary_version`.

### `data/source_assessment.csv`

Valutazione preliminare per territorio (unità di riferimento, corrispondenza, esito atteso, passo successivo).

### `data/sources.csv`

Registro delle fonti utilizzate per giustificare l'estensione di ciascun territorio.

## Fasi previste

1. Consolidamento della struttura e dell'anagrafica.
2. Ricerca e valutazione delle fonti.
3. Popolamento dei territori definibili tramite elenchi di comuni.
4. Costruzione documentata di poligoni ad hoc per i territori selezionati che restano irrisolti.

## Avvertenza

I nomi, le tipologie e le macroaree sono una bozza editoriale. Non costituiscono una classificazione ufficiale né certificano che il perimetro di ciascun territorio sia condiviso da tutte le fonti.
