{% regroup object_list by node as grupos %}
{% for grupo in grupos %}
{{grupo.grouper}}
{% for object in grupo.list %}
* [{{object.title}}]({{object.url}}) {% endfor %}
{% endfor %}
