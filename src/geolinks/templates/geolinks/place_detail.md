Ver /world {% for parent in object.parents %} {{parent.name}} /{{parent.slugq}}{% endfor %}

{% if object.place_set.count or object.uri_set.count %}Estos son los contenidos que hay en {{object.name}}: 
{% if object.place_set.count %}{% regroup object.place_set.all by subdivision as subdivisions %} 
{% for subdivision in subdivisions %}{% if subdivision.list %}
Por {{subdivision.grouper}}:{% for child in subdivision.list %}
/{{child.slugq}} {{child.name}} ({{child.uris}}){% endfor %}{% endif %}
{% endfor %}
{% endif %}

{% if object.uri_set.count %}
{{object.uris}} recursos disponibles:
{% for uri in object.uri_set.all %}
[{{uri.title}}]({{uri.url}}) {{uri.description}}{% endfor %}{% endif %}
{% else %}
No hay contenidos en {{object.name}}
{% endif %}
