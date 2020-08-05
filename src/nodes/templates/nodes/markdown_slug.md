# {{object.title}}
{{ object.text|default:"" }}
{% for uri in object.uri_set.all %}
* [{{uri.title}}]({{ uri.url }}){% endfor %}
{% regroup object.node_set.with_data.all by subdivision as subdivisions %}
{% for subdivision in subdivisions %}
## {{subdivision.grouper}}
{% for child in subdivision.list %}
### {{child.title}}
{% for uri in child.uri_set.all %}
* [{{uri.title}}]({{ uri.url }}){% endfor %}
{% for subchild in child.node_set.with_data.all %}* {{subchild.title}}:{% for uri in subchild.uri_set.all %}
    * [{{uri.title}}]({{ uri.url }}){% endfor %}
{% endfor %}{% endfor %}
{% endfor %}
