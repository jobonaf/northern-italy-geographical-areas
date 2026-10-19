# Territori geografici del Nord Italia

Repertorio in costruzione di territori geografici riconoscibili del Nord Italia, destinato ad analisi territoriali e applicazioni GIS.

## Stato del progetto

Il repository si trova nella **fase 1: struttura e anagrafica**. I 70 record attualmente presenti sono candidati iniziali e non rappresentano ancora delimitazioni validate. In questa fase non sono assegnati comuni e non sono inclusi poligoni.

## Criteri

- I territori sono selezionati in base alla loro riconoscibilità geografica, storica o culturale.
- Le delimitazioni possono sovrapporsi.
- Un territorio che attraversa più regioni amministrative mantiene un unico identificativo.
- I laghi considerati come entità autonome e i territori liguri sono esclusi dal repertorio corrente.
- Non vengono ricostruiti elenchi di comuni in assenza di fonti documentate.
- Fonti e criteri di delimitazione sono registrati separatamente dai dati derivati.

## Struttura del repository

```text
.
├── README.md
├── LICENSE
├── data/
│   ├── territories.csv
│   ├── territory_municipalities.csv
│   └── sources.csv
├── docs/
│   └── data-model.md
└── scripts/
    └── validate.py
```

## Tabelle

### `data/territories.csv`

Contiene una riga per territorio. `territory_id` è un identificativo interno stabile: non codifica confini amministrativi e non deve essere riutilizzato per un altro territorio.

Campi principali:

- `territory_type`: classificazione descrittiva provvisoria;
- `macro_area`: raggruppamento editoriale usato per organizzare il lavoro, non una delimitazione amministrativa;
- `status`: stato della verifica della delimitazione (`pending`, `defined`, `unresolved`);
- `boundary_method`: metodo adottato per definire il territorio, da compilare dopo la verifica;
- `notes`: osservazioni e questioni ancora da verificare.

### `data/territory_municipalities.csv`

Tabella relazionale con una riga per ogni associazione tra territorio e comune. I codici ISTAT saranno aggiunti dopo la scelta di una versione documentata dei confini e dei codici comunali.

### `data/sources.csv`

Registro delle fonti usate per documentare e giustificare l'estensione di ciascun territorio.

Per la descrizione completa delle tabelle, dei campi e delle relazioni si rimanda a [`docs/data-model.md`](docs/data-model.md).

## Fasi previste

1. Consolidamento della struttura e dell'anagrafica.
2. Ricerca e valutazione delle fonti.
3. Popolamento dei territori definibili mediante elenchi documentati di comuni.
4. Costruzione documentata di poligoni ad hoc per i territori selezionati che restano irrisolti.

## Avvertenza

Nomi, tipologie e macroaree costituiscono una bozza editoriale. Non rappresentano una classificazione ufficiale e non certificano che il perimetro di ciascun territorio sia condiviso da tutte le fonti.

## Licenza

Il contenuto del repository è distribuito secondo i termini indicati nel file [`LICENSE`](LICENSE).
