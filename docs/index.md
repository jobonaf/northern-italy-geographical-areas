---
layout: page
title: 70 territori del Nord Italia
---

Un’anagrafica aperta dei territori geografici del Nord Italia, con la provenienza di ogni confine. Clicca un territorio per vedere i dettagli.

{% include mappa.html %}

{% assign tutti = site.data.territori.features %}
{% assign con_confine = tutti | where_exp: "f", "f.geometry" %}
{% assign aperti = tutti | where_exp: "f", "f.properties.status != 'defined'" %}

**{{ con_confine | size }}** territori su 70 hanno un confine sulla mappa; **{{ aperti | size }}** sono ancora da risolvere. Vedi [come si costruiscono i confini]({{ '/metodo' | relative_url }}) e [come contribuire]({{ '/contribuire' | relative_url }}).

Per esplorare comune per comune c’è anche la [mappa dettagliata con ricerca]({{ '/territories_map.html' | relative_url }}).
