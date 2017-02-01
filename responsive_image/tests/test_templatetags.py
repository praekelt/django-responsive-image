from django import template
from django.test import TestCase


class TemplateTagsTestCase(TestCase):

    def test_static_non_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture "images/static-non-lazy.png" "300,300x200" %}"""
        )
        result = t.render(template.Context({}))
        print result

    def test_static_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture "images/static-lazy.png" "300,300x200" lazy=True %}"""
        )
        result = t.render(template.Context({}))
        print result
