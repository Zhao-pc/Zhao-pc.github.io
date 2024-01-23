---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---
You can find my publications here: [Publications(up to 01/2024)](../files/List_of_publications.pdf). 
{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
