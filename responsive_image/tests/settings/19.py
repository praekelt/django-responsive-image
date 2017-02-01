import os
import glob


BASE_DIR = os.path.join(
    glob.glob(os.environ["VIRTUAL_ENV"] +  "/lib/*/site-packages")[0],
    "responsive_image"
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "responsive_image.db"
    }
}

ROOT_URLCONF = "responsive_image.tests.urls"

INSTALLED_APPS = (
    "responsive_image",
    "responsive_image.tests",
    "photologue",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.staticfiles",
)

SECRET_KEY = "SECRET_KEY"

STATIC_URL = "/"
MEDIA_URL = "/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
