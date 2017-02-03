Django Responsive Image
=======================

.. figure:: https://travis-ci.org/praekelt/django-responsive-image.svg?branch=develop
   :align: center
   :alt: Travis

   Travis

Overview
--------

Django Responsive Image (DRI) provides a template tag that renders HTML5 markup
containing the ``picture`` tag and the ``srcset`` attribute.

It handles both static images and Photologue ImageModel derived objects. The static images
are not scaled by the system, but ImageModel objects are because that is the core purpose
of Photologue.

The Photologue support is optional.

Installation
------------

1. Install or add ``django-responsive-image`` to your Python path.
2. Add ``layers`` after ``responsive_image`` to your ``INSTALLED_APPS`` setting.
3. Optionally install ``django-photologue``.

Examples
--------

Static image with no lazy loading::

    {% picture "images/foo.png" "640,320x240" %}

Yields::

    <picture class="Picture">
        <!--[if IE 9]><video style="display: none;"><![endif]-->
        <!--[if IE 9]></video><![endif]-->
        <img class="Picture-image"
             src="/images/static-non-lazy.png"
             srcset="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
             data-sizes="auto"
        />
    </picture>

    <noscript>
        <img class="Picture-image"
             src="/images/static-non-lazy.png"
             srcset="/images/static-non-lazy-640.png 640w,
                     /images/static-non-lazy-320x240.png 320w 240h"
        />
    </noscript>


ImageModel (sub)object with no lazy loading::

    {% picture object "640,320x240" "detail,thumb" %}

Yields::

    <picture class="Picture">
        <!--[if IE 9]><video style="display: none;"><![endif]-->
        <!--[if IE 9]></video><![endif]-->
        <img class="Picture-image"
             srcset="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
             data-sizes="auto"
             alt="MyModel object"
        />
    </picture>

    <noscript>
        <img class="Picture-image"
             alt="MyModel object"
             srcset="/photologue/photos/cache/image_FBqACfc_detail.jpg 640w,
                    /photologue/photos/cache/image_FBqACfc_thumb.jpg 320w 240h"
        />
    </noscript>

Template tag arguments
----------------------

    * object_or_path - ImageModel (sub(object or path to a static file
    * sizes - comma delimited string of viewport sizes of the form WxH,W. H is optional.
    * size_names - comma delimited string of Photologue Size names that correspond to the viewport sizes. Required if object_or_path is an object.
    * classes - additional classes to inject on the ``<img>`` after the ``.Picture-image`` class.
    * lazy - boolean indicating whether the picture is lazily loaded. Default to false.

