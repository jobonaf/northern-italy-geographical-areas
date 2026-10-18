# Territori geografici del Nord Italia

Repertorio in costruzione di territori geografici riconoscibili del Nord Italia, pensato per analisi territoriali e uso GIS.

## Stato del progetto

I 70 territori sono candidati iniziali. Le fonti sono state cercate per 42 territori (Trentino-Alto Adige, Friuli-Venezia Giulia, Emilia-Romagna, Veneto); mancano Lombardia e Piemonte e Valle d'Aosta. Nessun comune è ancora assegnato e nessun poligono è incluso.

## Criteri

- I territori sono selezionati per riconoscibilità geografica, storica o culturale.
- Le delimitazioni possono sovrapporsi.
- Un territorio che attraversa più regioni amministrative mantiene un solo identificativo.
- I laghi come entità autonome e i territori liguri sono esclusi.
- Non si inventano elenchi di comuni per colmare lacune documentali.
- Si registrano solo fonti che contengono un elenco di comuni o uno strato GIS.
- Versione dei confini comunali ISTAT: da indicare qui con la data di riferimento al primo popolamento di `territory_municipalities.csv`.

## Struttura

```text
.
├── data/
│   ├── territories.csv
│   ├── sources.csv
│   └── territory_municipalities.csv
├── docs/
│   ├── data-model.md
│   └── id-migration.csv
├── scripts/validate.py
├── CHANGELOG.md
├── CITATION.cff
└── LICENSE
```

I campi e le regole sono in [`docs/data-model.md`](docs/data-model.md). I controlli si eseguono con `python3 scripts/validate.py`.

## Avvertenza

I nomi sono una bozza editoriale. Non costituiscono una classificazione ufficiale né certificano che il perimetro di ciascun territorio sia condiviso da tutte le fonti.
