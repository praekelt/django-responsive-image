import re

from django import template
from django.conf import settings
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils.functional import Promise


register = template.Library()


@register.tag
def picture(parser, token):
    tokens = token.split_contents()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError(
            """{% picture path
                  "W,WxH;W,WxH..."
                  [breakpoints=768,2014...]
                  [lazy=bool]
                  [classes=css-cls-1 css-cls-2]
               %}
            or
            {% picture object
               "W,WxH;W,WxH...."
               size_names="thumb,detail;hres,lres..."
               breakpoints=768,1024,...]
               [lazy=bool]
               [classes=css-cls-1 css-cls-2]
            %}
            """
        )

    kwargs = {}
    for token in tokens[3:]:
        li = token.split("=")
        if len(li) > 1:
            kwargs[li[0]] = li[1]

    return PictureNode(*tokens[1:3], **kwargs)


class PictureNode(template.Node):

    def __init__(self, object_or_path, sizes, **kwargs):
        self.object_or_path = template.Variable(object_or_path)
        self.sizes = template.Variable(sizes)
        self.kwargs = {}
        for k, v in kwargs.items():
            self.kwargs[k] = template.Variable(v)

    def render(self, context):
        object_or_path = self.object_or_path.resolve(context)
        sizes = self.sizes.resolve(context)

        # Resolve the kwargs
        resolved = {}
        for k, v in self.kwargs.items():
            r = v.resolve(context)
            if isinstance(r, Promise):
                r = unicode(r)
            resolved[k] = r

        # Parse sizes
        sources = []
        for group in sizes.split(";"):
            srcset = []
            for part in group.split(","):
                li = part.split("x")
                di = {"width": li[0], "height": ""}
                if len(li) > 1:
                    di["height"] = li[1]
                di["wh"] = di["width"] + "w"
                if di["height"]:
                    di["wh"] = di["wh"] + " " + di["height"] + "h"
                srcset.append(di)
            sources.append({"srcset": srcset, "breakpoint": None})

        # Parse breakpoints
        for n, bp in enumerate(resolved.get("breakpoints", "").split(",")):
            sources[n]["breakpoint"] = bp

        # Set URLs and object
        obj = None

        # Static image has a naming convention
        if isinstance(object_or_path, basestring):
            canonical_url = settings.STATIC_URL + object_or_path
            name, extension = canonical_url.rsplit(".", 1)
            for source in sources:
                for di in source["srcset"]:
                    url = "%s-%s" % (name, di["width"])
                    if di["height"]:
                        url = url + "x" + di["height"]
                    url = url + "." + extension
                    di["url"] = url

        # Photologue ImageModel (sub)object follows photologue names
        elif isinstance(object_or_path, Model):
            obj = object_or_path
            canonical_url = obj.image.url
            name, extension = canonical_url.rsplit(".", 1)

            # We can get away with splitting on "," or ";". Makes algorithm
            # simpler.
            size_names = re.split(r"[,;]", resolved.get("size_names", ""))
            n = 0
            for source in sources:
                for di in source["srcset"]:
                    url = getattr(obj, "get_%s_url" % size_names[n])()
                    di["url"] = url
                    n += 1

        else:
            raise RuntimeError, "object_or_path has invalid type"

        # Flatten sources because template needs it and code is faster here
        srcsets = []
        for source in sources:
            srcsets.extend(source["srcset"])

        canonical_url_name, canonical_url_extension = canonical_url.rsplit(".", 1)
        return render_to_string(
            "responsive_image/inclusion_tags/picture.html",
            {
                "object": obj,
                "canonical_url": canonical_url,
                "sources": sources,
                "srcsets": srcsets,
                "lazy": resolved.get("lazy", False),
                "classes": resolved.get("classes", False)
            }
        )
