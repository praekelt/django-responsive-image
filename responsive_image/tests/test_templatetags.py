import os
from shutil import rmtree

from django import template
from django.conf import settings
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

        # Clean the media root
        if os.path.exists(settings.MEDIA_ROOT):
            rmtree(settings.MEDIA_ROOT)

        # Create test object
        cls.obj = MyModel.objects.create()
        set_image(cls.obj)

    def test_static_non_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture "images/static-non-lazy.png" "640,320x240" %}"""
        )
        result = t.render(template.Context({}))
        self.failUnless("/images/static-non-lazy-640.png 640w" in result)
        self.failUnless("/images/static-non-lazy-320x240.png 320w 240h" in result)

    def test_static_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture "images/static-lazy.png" "640,320x240" lazy=True %}"""
        )
        result = t.render(template.Context({}))
        self.failUnless("<source data-srcset=" in result)
        self.failUnless("/images/static-lazy-640.png 640w" in result)
        self.failUnless("/images/static-lazy-320x240.png 320w 240h" in result)

    def test_photologue_non_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture object "640,320x240" "detail,thumb" %}"""
        )
        result = t.render(template.Context({"object": self.obj}))
        self.failUnless("/photologue/photos/cache/image_detail.jpg 640w" in result)
        self.failUnless("/photologue/photos/cache/image_thumb.jpg 320w 240h" in result)

    def test_photologue_lazy(self):
        t = template.Template("""{% load responsive_image_tags %}
            {% picture object "640,320x240" "detail,thumb" lazy=True %}"""
        )
        result = t.render(template.Context({"object": self.obj}))
        self.failUnless("<source data-srcset=" in result)
        self.failUnless("/photologue/photos/cache/image_detail.jpg 640w" in result)
        self.failUnless("/photologue/photos/cache/image_thumb.jpg 320w 240h" in result)
