---
layout: page
title: Contribuire
permalink: /contribuire/
---

Serve soprattutto una cosa: una fonte che dica quali comuni compongono un territorio.

1. Scegli un territorio dall’elenco qui sotto.
2. Trova un documento che lo definisce (un atto, un sito istituzionale, una pubblicazione).
3. Apri una segnalazione con il link e, se la fonte li elenca, i comuni con codice ISTAT.

Se la fonte non elenca i comuni, il territorio resta da risolvere: non li assegniamo per analogia.

## Territori ancora da risolvere

{% assign aperti = site.data.territori.features | where_exp: "f", "f.properties.status != 'defined'" %}
{% if aperti.size == 0 %}
L’elenco compare quando i dati sono pubblicati.
{% else %}
{% for f in aperti %}
- [{{ f.properties.name }}]({{ site.repo_url }}/issues/new?title={{ 'Fonte per: ' | append: f.properties.name | url_encode }})
{% endfor %}
{% endif %}

[Apri una segnalazione]({{ site.repo_url }}/issues/new) · [Vai al repository]({{ site.repo_url }})
