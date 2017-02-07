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

    <picture class="Picture Picture--cover">
        <!--[if IE 9]><video style="display: none;"><![endif]-->
        <!--[if IE 9]></video><![endif]-->
        <img src="/images/foo.png"
             srcset="/images/foo-640.png 640w,
                     /images/foo-320x240.png 320w 240h"
        />
    </picture>

    <noscript>
        <img src="/images/foo.png"
             srcset="/images/foo-640.png 640w,
                     /images/foo-320x240.png 320w 240h"
        />
    </noscript>


ImageModel (sub)object with no lazy loading::

    {% picture object "640,320x240" size_names="detail,thumb" %}

Yields::

    <picture class="Picture Picture--cover">
        <!--[if IE 9]><video style="display: none;"><![endif]-->
        <!--[if IE 9]></video><![endif]-->
        <img src="/photologue/photos/image.jpg"
            alt="MyModel object"
            srcset="/photologue/photos/cache/image_detail.jpg 640w,
                    /photologue/photos/cache/image_thumb.jpg 320w 240h"
        />
    </picture>

    <noscript>
        <img src="/photologue/photos/image.jpg"
            alt="MyModel object"
            srcset="/photologue/photos/cache/image_detail.jpg 640w,
                    /photologue/photos/cache/image_thumb.jpg 320w 240h"
        />
    </noscript>

Static image with breakpoints and lazy loading::

    {% picture "images/foo.png" "640,320x240;1024" breakpoints="640,1024" lazy=True %}

Yields::

    <picture class="Picture Picture--cover">
        <!--[if IE 9]><video style="display: none;"><![endif]-->
        <source data-srcset="
            /images/foo-640.png 640w,
            /images/foo-320x240.png 320w 240h"
            media="(min-width: 640px)"
        />
        <source data-srcset="
            /images/foo-1024.png 1024w"
            media="(min-width: 1024px)"
        />
        <!--[if IE 9]></video><![endif]-->
        <img class="Picture-image lazyautosizes lazyloaded"
             srcset="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
             data-sizes="auto"
             alt="Responsive image"
         />
    </picture>

    <noscript>
        <img src="/images/foo.png"
             srcset="
                /images/foo-640.png 640w,
                /images/foo-320x240.png 320w 240h,
                /images/foo-1024.png 1024w"
        />
    </noscript>

ImageModel (sub)object with breakpoints and lazy loading::

    {% picture object "640,320x240;1024" breakpoints="640,1024" size_names="detail,thumb;retina" lazy=True %}

Yields::

    <picture class="Picture Picture--cover">
        <!--[if IE 9]><video style="display: none;"><![endif]-->
        <source data-srcset="
            /photologue/photos/cache/image_detail.jpg 640w,
            /photologue/photos/cache/image_thumb.jpg 320w 240h"
            media="(min-width: 640px)"
        />
        <source data-srcset="
            /photologue/photos/cache/image_retina.jpg 1024w"
            media="(min-width: 1024px)"
        />
        <!--[if IE 9]></video><![endif]-->
        <img class="Picture-image lazyautosizes lazyloaded"
             srcset="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
             data-sizes="auto"
             alt="MyModel object"
         />
    </picture>

    <noscript>
        <img src="/photologue/photos/image.jpg"
             alt="MyModel object"
             srcset="
                /photologue/photos/cache/image_detail.jpg 640w,
                /photologue/photos/cache/image_thumb.jpg 320w 240h,
                /photologue/photos/cache/image_retina.jpg 1024w"
        />
    </noscript>

Template tag arguments
----------------------

    * object_or_path - ImageModel (sub(object or path to a static file
    * sizes - comma and optional semi-colon delimited string of viewport sizes
      of the form WxH,W;WxH. H is optional. Use the semi-colon if you specify
      breakpoints.
    * breakpoints - optional comma delimited set of breakpoints.
    * size_names - comma and optional semi-colon delimited string of Photologue
      Size names that correspond to the viewport sizes. Use the semi-colon if
      you specify breakpoints. Required if object_or_path is an object.
    * lazy - boolean indicating whether the picture is lazily loaded. Defaults
      to false.

