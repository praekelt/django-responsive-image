import multiprocessing
from setuptools import setup, find_packages


setup(
    name="django-responsive-image",
    version="0.1",
    description="Provides a template tag that implements picture, srcset and lazy loading. Supports django-photologue.",
    long_description = open("README.rst", "r").read() + open("AUTHORS.rst", "r").read() + open("CHANGELOG.rst", "r").read(),
    author="Praekelt Consilting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="http://github.com/praekelt/django-responsive-image",
    packages = find_packages(),
    install_requires = [
        "django",
        "django-photologue"
    ],
    include_package_data=True,
    tests_require=[
        "tox",
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
