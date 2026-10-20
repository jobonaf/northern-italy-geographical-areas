# Territori geografici del Nord Italia

Repertorio in costruzione di territori geografici riconoscibili del Nord Italia, destinato ad analisi territoriali e applicazioni GIS.

## Stato del progetto

Il repository e nella **fase 3: popolamento delle associazioni territorio-comune**.

Stato corrente dei dati, dopo gli ultimi aggiornamenti:

- 76 territori censiti;
- 93 fonti registrate;
- 1.410 associazioni territorio-comune;
- 62 territori `defined` (81,6%);
- 14 territori `pending`;
- 0 territori `unresolved`.

I territori `defined` dispongono di una lista documentata di comuni. I territori `pending` richiedono ancora una scelta del perimetro o una lista verificabile. Le delimitazioni possono sovrapporsi.

## Criteri

- I territori sono selezionati in base alla loro riconoscibilita geografica, storica o culturale.
- Un territorio che attraversa piu regioni amministrative mantiene un unico identificativo.
- Le sovrapposizioni e le relazioni di inclusione tra territori sono ammesse e conservate.
- Quando disponibile e coerente con il territorio adottato, si preferisce un perimetro SNAI per favorire l'omogeneita nazionale.
- Negli altri casi si usano elenchi istituzionali; fonti secondarie sono adottate solo quando la convenzione e esplicita e riproducibile.
- La versione corrente rappresenta i territori esclusivamente come aggregazioni di comuni interi.
- I territori non rappresentabili in modo soddisfacente mediante comuni restano `pending`.
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

Gli script temporanei usati per aggiungere, correggere o migrare gruppi di territori non fanno parte del repository.

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
- `notes`: nome del comune o eventuali osservazioni sull'associazione.

Uno stesso comune puo appartenere a piu territori.

### `data/sources.csv`

Registro delle fonti usate per documentare le liste comunali. Per la descrizione completa delle tabelle e delle relazioni si rimanda a [docs/data-model.md](docs/data-model.md).

## Validazione

Dalla radice del repository:

```powershell
py scripts/validate.py
```

Il validatore controlla intestazioni, identificativi, stati, duplicati, chiavi esterne, codici ISTAT, URL e date. Restituisce inoltre lo stato di avanzamento, per esempio:

```text
76 territori, 93 fonti, 1410 associazioni; 0 problemi
Avanzamento: 62/76 territori defined (81.6%); 14 pending; 0 unresolved
```

## Mappa interattiva

Lo script `scripts/map_territories.py` rappresenta i comuni associati ai territori `defined`. Ogni territorio usa un colore distinto; la trasparenza rende visibili le sovrapposizioni. La mappa include tooltip, ricerca per comune, controllo dei layer e modalita a schermo intero.

Lo script non corregge o sostituisce codici: rappresenta esclusivamente quanto registrato nei CSV. Tutti i codici ISTAT devono quindi essere presenti nello shapefile comunale utilizzato.

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

Per generare la mappa, avviare un server locale e aprire automaticamente il browser:

```powershell
py scripts/map_territories.py --serve
```

L'output predefinito e `output/territories_map.html`. Se la porta predefinita e occupata:

```powershell
py scripts/map_territories.py --serve --port 8766
```

Sfondi disponibili, senza API key:

```powershell
py scripts/map_territories.py --tiles osm --serve
py scripts/map_territories.py --tiles opentopomap --serve
py scripts/map_territories.py --tiles none --serve
```

`osm` e `opentopomap` richiedono una connessione quando la pagina viene visualizzata. L'opzione `none` non usa tessere remote.

Percorsi alternativi possono essere indicati esplicitamente:

```powershell
py scripts/map_territories.py `
  --shapefile "D:\dati\comuni.shp" `
  --data-dir data `
  --output output\territories_map.html `
  --serve
```

## Fasi di lavoro

- Consolidamento della struttura e dell'anagrafica: completato.
- Ricerca e valutazione delle fonti: copertura di base completata, approfondimenti ancora in corso.
- Popolamento mediante elenchi documentati di comuni: in corso.
- Revisione cartografica e correzione delle associazioni nome-codice: in corso.
- Acquisizione di geometrie indipendenti dai comuni: non prevista nella fase corrente.

## Avvertenza

Le delimitazioni adottate sono convenzioni operative documentate. Non certificano che il perimetro di ciascun territorio sia condiviso da tutte le fonti. L'uso di comuni interi puo sovrastimare territori che interessano soltanto porzioni comunali. Le versioni dei confini amministrativi e le fusioni comunali devono essere considerate quando si confrontano dati e geometrie di date diverse.

## Licenza

Il contenuto del repository e distribuito secondo i termini indicati nel file [LICENSE](LICENSE).
