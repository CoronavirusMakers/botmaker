{% for node in object_list %}
## {% for parent in node.parents %}{{parent}} | {% endfor %}{{node}}
{% for object in node.uri_set.all %}
* [{{object.title}}]({{object.url}}) {% endfor %}
{% endfor %}
