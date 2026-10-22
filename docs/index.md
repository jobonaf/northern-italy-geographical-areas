---
layout: page
title: Territori geografici del Nord Italia
---

Un’anagrafica aperta dei territori geografici del Nord Italia, con la provenienza di ogni confine. La mappa mostra i territori con un confine comunale già definito; la tabella comprende anche quelli ancora da definire.

{% include mappa.html %}

{% assign tutti = site.data.territori.features %}
{% assign con_confine = tutti | where_exp: "f", "f.geometry" %}
{% assign aperti = tutti | where_exp: "f", "f.properties.status != 'defined'" %}

Sono censiti **{{ tutti | size }} territori**: **{{ con_confine | size }}** hanno un confine disponibile e **{{ aperti | size }}** sono ancora da definire. Vedi [come si costruiscono i confini]({{ '/metodo' | relative_url }}) e [come contribuire]({{ '/contribuire' | relative_url }}).

## Tabella di sintesi

La tabella riporta stato, numero di comuni, note e fonte, quando disponibile. Il collegamento **Segnala modifica** permette di proporre correzioni per qualsiasi territorio, compresi quelli già definiti.

{% include tabella_territori.html %}

Per esplorare comune per comune è disponibile anche la [mappa dettagliata con ricerca]({{ '/territories_map.html' | relative_url }}).
