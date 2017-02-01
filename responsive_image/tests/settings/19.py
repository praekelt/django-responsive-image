import os
import glob


BASE_DIR = os.path.join(
    glob.glob(os.environ["VIRTUAL_ENV"] +  "/lib/*/site-packages")[0],
    "layers"
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "layers.db"
    }
}

ROOT_URLCONF = "layers.tests.urls"

INSTALLED_APPS = (
    "layers",
    "layers.tests",
    "layers.tests.someapp",
    "crum",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.staticfiles",
)

SECRET_KEY = "SECRET_KEY"

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "crum.CurrentRequestUserMiddleware",
)

# Layers loaders must precede default equivalent loaders
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, "tests", "templates")
        ],
        "OPTIONS": {
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven"t customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                # insert your TEMPLATE_LOADERS here
                "layers.loaders.filesystem.Loader",
                "django.template.loaders.filesystem.Loader",
                "layers.loaders.app_directories.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
]

STATICFILES_FINDERS = (
    "layers.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "layers.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_DIRS = (os.path.join(BASE_DIR, "tests", "static"),)

STATIC_URL = "/"
STATIC_ROOT = os.path.join(BASE_DIR, "tmp")

LAYERS = {"layers": ["basic"]}
