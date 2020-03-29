{% load botmaker %}\*{{object.title}}\*

{% if object.text %}{{object.text}}

{% endif %}{% regroup object.node_set.with_data.all by subdivision as subdivisions %}{% for subdivision in subdivisions %}{% if subdivision.list %} Por {{subdivision.grouper}}:{% for child in subdivision.list %}
/{{child.slug|quote_telegram}} {{child.title}} ({{child.uris}}){% endfor %}{% endif %}

{% endfor %}{% if object.uri_set.exists %}{{object.uri_set.count}} recursos disponibles:
{% for uri in object.uri_set.all %}- [{{uri.title}}]({{uri.url}}) {{uri.text|default:""}}
{% endfor %}{% endif %}
