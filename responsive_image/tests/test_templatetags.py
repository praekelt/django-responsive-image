import os

from django import template
from django.core.files.base import ContentFile
from django.test import TestCase

from responsive_image.tests.models import MyModel


RES_DIR = os.path.join(os.path.dirname(__file__), "res")
IMAGE_PATH = os.path.join(RES_DIR, "image.jpg")


def set_image(obj):
    obj.image.save(
        os.path.basename(IMAGE_PATH),
        ContentFile(open(IMAGE_PATH, "rb").read())
    )


class TemplateTagsTestCase(TestCase):
    fixtures = ["photosizes.json"]

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsTestCase, cls).setUpTestData()
        cls.obj = MyModel.objects.create()
        set_image(cls.obj)

    def test_static_non_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture "images/static-non-lazy.png" "640,320x240" %}"""
        )
        result = t.render(template.Context({}))
        print result

    def test_static_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture "images/static-lazy.png" "640,320x240" lazy=True %}"""
        )
        result = t.render(template.Context({}))
        print result

    def test_photologue_non_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture object "640,320x240" "detail,thumb" %}"""
        )
        result = t.render(template.Context({"object": self.obj}))
        print result

    def test_photologue_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture object "640,320x240" "detail,thumb" lazy=True %}"""
        )
        result = t.render(template.Context({"object": self.obj}))
        print result

