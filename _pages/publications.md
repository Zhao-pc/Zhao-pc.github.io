---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---
You can find my publications here: [Publications](../files/List_of_publications.pdf) (up to 01/2024) and [Google Scholar](https://scholar.google.com.hk/citations?user=tUOE-8IAAAAJ&hl=zh-CN). 
 {%if author.googlescholar %}
  {%You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>%}
{% endif %}

{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
