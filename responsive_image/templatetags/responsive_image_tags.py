from django import template
from django.conf import settings
from django.template.loader import render_to_string


register = template.Library()


@register.tag
def picture(parser, token):
    tokens = token.split_contents()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError(
            """{% picture path "W,WxH,..." [lazy=bool] %}
            or
            {% picture object "W,WxH,..." "thumb,detail" [lazy=bool] %}
            """
        )

    # Some inelegant parsing
    kwargs = {"lazy": None}
    if "lazy=" in tokens[-1]:
        kwargs["lazy"] = tokens[-1].split("=")[1]
        args = tokens[1:-1]
    else:
        args = tokens[1:]

    return PictureNode(*args, **kwargs)


class PictureNode(template.Node):

    def __init__(self, object_or_path, sizes, size_names=None, lazy=None):
        self.object_or_path = template.Variable(object_or_path)
        self.sizes = template.Variable(sizes)
        self.size_names = None
        if size_names is not None:
            self.size_names = template.Variable(size_names)
        self.lazy = None
        if lazy is not None:
            self.lazy = template.Variable(lazy)

    def render(self, context):
        object_or_path = self.object_or_path.resolve(context)
        sizes = self.sizes.resolve(context)
        if self.size_names is not None:
            size_names = self.size_names.resolve(context)
        else:
            size_names = ""
        if self.lazy is not None:
            lazy = self.lazy.resolve(context)
        else:
            lazy = False

        # Parse sizes. Let errors propagate.
        srcsets = []
        for part in sizes.split(","):
            li = part.split("x")
            di = {"width": li[0], "height": 0}
            if len(li) > 1:
                di["height"] = li[1]
            srcsets.append(di)

        # Set URLs and object
        obj = None
        if isinstance(object_or_path, basestring):
            canonical_url = "%s%s" % (settings.STATIC_URL, object_or_path)
            for di in srcsets:
                url = "%s-%s" % (object_or_path, di["width"])
                if di["height"]:
                    url = "%s%sx%s" % (settings.STATIC_URL, url, di["height"])
        elif isinstance(object_or_path, models.Model):
            obj = object_or_path
            canonical_url = obj.image.url
        else:
            raise RuntimeError, "object_or_path has invalid type"

        canonical_url_name, canonical_url_extension = canonical_url.rsplit(".", 1)
        return render_to_string(
            "responsive_image/inclusion_tags/picture.html",
            {
                "object": obj,
                "canonical_url": canonical_url,
                "canonical_url_name": canonical_url_name,
                "canonical_url_extension": canonical_url_extension,
                "srcsets": srcsets,
                "lazy": lazy
            }
        )
