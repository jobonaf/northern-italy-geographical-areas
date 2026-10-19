# Territori geografici del Nord Italia

Repertorio in costruzione di territori geografici riconoscibili del Nord Italia, destinato ad analisi territoriali e applicazioni GIS.

## Stato del progetto

Il repository e nella **fase 3: popolamento delle associazioni territorio-comune**.

Stato corrente dei dati:

- 70 territori censiti;
- 87 fonti registrate;
- 756 associazioni territorio-comune;
- 28 territori `defined` (40,0%);
- 42 territori `pending`;
- 0 territori `unresolved`.

I territori `defined` dispongono di una lista documentata di comuni. I territori `pending` richiedono ancora una scelta del perimetro, una lista verificabile o uno strato cartografico. Le delimitazioni possono sovrapporsi.

## Criteri

- I territori sono selezionati in base alla loro riconoscibilita geografica, storica o culturale.
- Un territorio che attraversa piu regioni amministrative mantiene un unico identificativo.
- Le sovrapposizioni tra territori sono ammesse e conservate nel modello.
- Quando disponibile e coerente con il territorio adottato, si preferisce un perimetro SNAI per favorire l'omogeneita nazionale.
- Negli altri casi si usano elenchi istituzionali; fonti secondarie sono adottate solo quando la convenzione e esplicita e riproducibile.
- I territori che interessano solo porzioni di comuni richiedono preferibilmente uno strato GIS e restano `pending` finche il perimetro non e acquisito.
- I laghi considerati come entita autonome e i territori liguri sono esclusi dal repertorio corrente.

## Struttura del repository

```text
.
├── README.md
├── CHANGELOG.md
├── LICENSE
├── data/
│   ├── territories.csv
│   ├── territory_municipalities.csv
│   └── sources.csv
├── docs/
│   └── data-model.md
├── output/
│   └── territories_map.html       # generato, non necessariamente versionato
└── scripts/
    ├── validate.py
    └── map_territories.py
```

## Tabelle

### `data/territories.csv`

Contiene una riga per territorio:

- `territory_id`: slug interno stabile;
- `name`: nome leggibile;
- `status`: `pending`, `defined` oppure `unresolved`;
- `notes`: criterio adottato o questione ancora aperta.

### `data/territory_municipalities.csv`

Tabella relazionale con una riga per ogni associazione tra territorio e comune:

- `territory_id`: riferimento a `territories.csv`;
- `istat_code`: codice ISTAT comunale a sei cifre;
- `source_id`: fonte del perimetro adottato;
- `notes`: eventuali osservazioni sull'associazione.

Uno stesso comune puo appartenere a piu territori.

### `data/sources.csv`

Registro delle fonti usate per documentare liste comunali e strati GIS. Per la descrizione completa delle tabelle e delle relazioni si rimanda a [`docs/data-model.md`](docs/data-model.md).

## Validazione

Dalla radice del repository:

```powershell
py scripts/validate.py
```

Il validatore controlla intestazioni, identificativi, stati, duplicati, chiavi esterne, codici ISTAT, URL e date. Restituisce inoltre lo stato di avanzamento, ad esempio:

```text
70 territori, 87 fonti, 756 associazioni; 0 problemi
Avanzamento: 28/70 territori defined (40.0%); 42 pending; 0 unresolved
```

## Mappa interattiva

Lo script `scripts/map_territories.py` rappresenta i comuni associati ai territori `defined`. Ogni territorio usa un colore distinto; la trasparenza rende visibili le sovrapposizioni. La mappa include tooltip, ricerca per comune, controllo dei layer e modalita a schermo intero.

### Dipendenze

```powershell
py -m pip install pandas geopandas folium
```

### Dati geografici

Il percorso predefinito dello shapefile comunale e:

```text
C:\scratch\dati\geodata\ConfiniAmministrativi\Limiti01012026_g\Com01012026_g\Com01012026_g_WGS84.shp
```

Devono essere presenti anche i file `.dbf`, `.prj` e `.shx` con lo stesso nome di base.

### Esecuzione

```powershell
py scripts/map_territories.py
```

L'output predefinito e `output/territories_map.html`.

Sfondi disponibili, tutti senza API key:

```powershell
py scripts/map_territories.py --tiles osm
py scripts/map_territories.py --tiles opentopomap
py scripts/map_territories.py --tiles none
```

`osm` e `opentopomap` richiedono una connessione quando la pagina viene visualizzata; `none` non usa tessere remote.

Percorsi alternativi possono essere indicati esplicitamente:

```powershell
py scripts/map_territories.py `
  --shapefile "D:\dati\comuni.shp" `
  --data-dir data `
  --output output\territories_map.html
```

Lo script verifica che tutti i codici ISTAT siano presenti nello shapefile. Per fusioni successive alla data geometrica usa raccordi espliciti tra codici correnti e geometrie precedenti, come per Castegnero Nanto rispetto allo shapefile del 1 gennaio 2026.

## Fasi di lavoro

1. Consolidamento della struttura e dell'anagrafica: completato.
2. Ricerca e valutazione delle fonti: copertura di base completata, approfondimenti ancora in corso.
3. Popolamento mediante elenchi documentati di comuni: in corso.
4. Acquisizione o costruzione documentata dei poligoni per i territori non esprimibili mediante comuni: da avviare.

## Avvertenza

Le delimitazioni adottate sono convenzioni operative documentate. Non certificano che il perimetro di ciascun territorio sia condiviso da tutte le fonti. Le versioni dei confini amministrativi e le fusioni comunali devono essere considerate quando si confrontano dati e geometrie di date diverse.

## Licenza

Il contenuto del repository e distribuito secondo i termini indicati nel file [`LICENSE`](LICENSE).
