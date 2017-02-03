from django import template
from django.conf import settings
from django.db.models import Model
from django.template.loader import render_to_string


register = template.Library()


@register.tag
def picture(parser, token):
    tokens = token.split_contents()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError(
            """{% picture path "W,WxH,..." [classes="className"] [lazy=bool] %}
            or
            {% picture object "W,WxH,..." "thumb,detail" [classes="className"] [lazy=bool] %}
            """
        )

    # Some parsing
    parsed_args = []
    parsed_kwargs = {}
    for token in tokens[1:]:
        if '='in token:
            k, v = token.split('=')
            parsed_kwargs[k] = v
        else:
            parsed_args.append(token)

    return PictureNode(*parsed_args, **parsed_kwargs)


class PictureNode(template.Node):

    def __init__(self, object_or_path, sizes, size_names=None, classes=None, lazy=None):
        self.object_or_path = template.Variable(object_or_path)
        self.sizes = template.Variable(sizes)
        self.size_names = None
        if size_names is not None:
            self.size_names = template.Variable(size_names)
        self.lazy = None
        if lazy is not None:
            self.lazy = template.Variable(lazy)
        self.classes = None
        if classes is not None:
            self.classes = template.Variable(classes)

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
        if self.classes is not None:
            classes = self.classes.resolve(context)
        else:
            classes = ""

        # Parse sizes. Let errors propagate.
        srcsets = []
        for part in sizes.split(","):
            li = part.split("x")
            di = {"width": li[0], "height": ""}
            if len(li) > 1:
                di["height"] = li[1]
            di["wh"] = di["width"] + "w"
            if di["height"]:
                di["wh"] = di["wh"] + " " + di["height"] + "h"
            srcsets.append(di)

        # Set URLs and object
        obj = None

        # Static image has a naming convention
        if isinstance(object_or_path, basestring):
            canonical_url = settings.STATIC_URL + object_or_path
            name, extension = canonical_url.rsplit(".", 1)
            for di in srcsets:
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

        # @hedley
        # Alternative solutions for this block:
        # only return pairs that have both values,
        # or only ask for photologue sizes if objects and get the dimensions from photologue?
            sizes = size_names.split(",")
            if len(sizes) == len(srcsets):
                for di, size_name in zip(srcsets, sizes):
                    url = getattr(obj, "get_%s_url" % size_name, None)
                    if url is None:
                        raise template.TemplateSyntaxError(
                            'The photo size  "%s" has not been defined in '
                            'photologue.photo_sizes.' % str(size_name)
                        )
                    di["url"] = url
            else:
                raise template.TemplateSyntaxError(
                        "equal size_names to srcsets arg values required "
                        "when using ImageModel value for object_or_path"
                    )

        else:
            raise RuntimeError, "object_or_path has invalid type"

        canonical_url_name, canonical_url_extension = canonical_url.rsplit(".", 1)
        return render_to_string(
            "responsive_image/inclusion_tags/picture.html",
            {
                "object": obj,
                "canonical_url": canonical_url,
                "srcsets": srcsets,
                "lazy": lazy,
                "classes": classes
            }
        )
