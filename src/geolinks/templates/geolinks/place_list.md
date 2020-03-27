Recursos a nivel mundial:
{% regroup object_list by subdivision as subdivisions %}{% for subdivision in subdivisions %}
{{subdivision.grouper}}:{% for country in subdivision.list %}
/{{country.slug}} {{country.name}} ({{country.uris}}){% endfor %}{% endfor %}
