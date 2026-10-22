---
layout: page
title: Metodo
permalink: /metodo/
---

Ogni territorio ha un identificativo stabile, un nome canonico, una tipologia e una macroarea. I confini si ricavano in quattro fasi, ciascuna con un risultato verificabile.

{% for f in site.data.fasi %}
### {{ forloop.index }}. {{ f.titolo }} ({{ f.stato }})

{{ f.testo }}
{% endfor %}

## Due regole che non si piegano

**Nessuna copertura forzata.** Un territorio senza fonte adeguata resta “da risolvere”. Non assegniamo comuni per analogia o intuizione.

**La fonte non è il risultato.** La fonte documenta il territorio; l’elenco dei comuni è la sua rappresentazione operativa. Le divergenze tra le due si registrano.

## Provenienza dei dati

Ogni geometria porta con sé provenienza e metodo, e distingue i confini ufficiali da quelli ricostruiti. Il campo `boundary_version` indica a quale versione dei confini comunali ISTAT si riferisce, così le geometrie si possono rifare in futuro. Il risultato finale è un GeoPackage.
