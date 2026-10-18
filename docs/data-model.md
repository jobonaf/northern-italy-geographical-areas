# Modello dati (proposta semplificata)

Il modello descrive i territori e le delimitazioni adottate. La ricerca delle fonti è lavoro preparatorio: nel repository restano solo le fonti che servono a produrre una delimitazione.

## File

Tre CSV in `data/`, codifica UTF-8, fine riga LF.

### `territories.csv`

| Campo | Contenuto |
|---|---|
| `territory_id` | Slug stabile, minuscolo, senza accenti, mai riutilizzato. |
| `name` | Nome canonico. |
| `status` | `pending`, `defined` oppure `unresolved`. |
| `notes` | Facoltativo. Decisioni, ambiguità e piste di ricerca. |

Significato dello stato:
- `pending`: non ancora esaminato fino in fondo.
- `defined`: esiste un elenco di comuni in `territory_municipalities.csv`.
- `unresolved`: nessuna fonte adeguata; non si assegnano comuni per analogia.

Se un territorio non ha fonti registrate, la pista di ricerca va in `notes` (per esempio «distretto sociale della Comunità Pusteria»).

### `sources.csv`

| Campo | Contenuto |
|---|---|
| `source_id` | `S0001`, `S0002`… Stabile e mai riutilizzato. Dopo le eliminazioni restano buchi nella numerazione, senza rinumerare. |
| `territory_id` | Territorio documentato. Una fonte che riguarda più territori compare su più righe. |
| `title` | Titolo del documento, con l'ente se non evidente. |
| `url` | Indirizzo della fonte. |
| `source_type` | `list` (elenco di comuni), `gis` (strato geografico) oppure `both`. |
| `access_date` | Data di consultazione, `AAAA-MM-GG`. |
| `notes` | Cosa documenta, limiti, copie non ufficiali, versione dei comuni usata. |

Regola di registrazione: si registra una fonte solo se contiene un elenco di comuni o uno strato GIS. Fonti che citano solo il nome del territorio, il numero dei comuni o enti amministrativi non vanno registrate.

### `territory_municipalities.csv`

| Campo | Contenuto |
|---|---|
| `territory_id` | Riferimento a `territories.csv`. |
| `istat_code` | Codice ISTAT del comune, sei cifre. |
| `source_id` | Facoltativo. Fonte da cui deriva l'inclusione. |
| `notes` | Facoltativo. Eccezioni motivate, per esempio comune incluso solo in parte. |

Le righe sono i soli comuni inclusi. Ipotesi scartate e comuni esclusi stanno nelle note delle fonti o nella cronologia Git.

## Esempi

```csv
territory_id,name,status,notes
val-venosta,Val Venosta,pending,"Comunità comprensoriale; Naturno, Parcines e Plaus esclusi (Burgraviato)"
val-badia,Val Badia,pending,"Distretto sociale della Comunità Pusteria: cercare l'elenco dei comuni"
```

```csv
source_id,territory_id,title,url,source_type,access_date,notes
S0033,carso,Partecipazioni del GAL del Carso (UTI Giuliana),https://example.org/doc.pdf,list,2026-10-17,"Elenca i comuni soci del GAL, non l'area"
```

## Controlli di `scripts/validate.py`

- `territory_id` e `source_id` univoci; slug valido.
- `status` tra i tre valori ammessi; `defined` solo se esiste almeno un comune.
- `territory_id` presente in `territories.csv` in tutte le tabelle.
- `istat_code` di sei cifre; nessuna associazione duplicata.
- `source_type` tra `list`, `gis`, `both`; `source_id` esistente quando indicato.

## Cosa viene eliminato

- Da `territories.csv`: `territory_type`, `macro_area`, `boundary_method`.
- Da `sources.csv`: `publisher`, `evidence`, `source_class`, `lists_municipalities` (le informazioni utili passano in `notes`).
- Da `territory_municipalities.csv`: `inclusion_status`, `boundary_version`.
- Interi file: `source_assessment.csv`, `boundary_versions.csv`.

## Da fissare nel README

- La versione dei confini comunali ISTAT usata (una riga, con la data di riferimento), finché non servono più edizioni confrontabili.
- La documentazione e il CHANGELOG vanno riscritti sul nuovo modello, mantenendo `docs/id-migration.csv` finché serve.
