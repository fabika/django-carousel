from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from carousel.models import Carousel

register = template.Library()


def __do_carousel(token, search_field_name):
    """
    {% carousel $carousel_obj [max_items] %}
    """
    bits = token.split_contents()
    search_field_value = bits[1]
    max_items = bits[2] if len(bits) > 2 else None
    return CarouselNode(max_items=max_items, **{search_field_name: search_field_value})


@register.tag('carousel')
def do_carousel(parser, token):
    return __do_carousel(token, 'object')


@register.tag('carousel_with_name')
def do_carousel_with_name(parser, token):
    return __do_carousel(token, 'name')


@register.tag('carousel_with_slug')
def do_carousel_with_slug(parser, token):
    return __do_carousel(token, 'slug')


@register.tag('carousel_with_id')
def do_carousel_with_id(parser, token):
    return __do_carousel(token, 'id')


class CarouselNode(template.Node):
    def __init__(self, object=None, name=None, slug=None, id=None, max_items=None):
        self.carousel_object = object
        self.carousel_name = name
        self.carousel_slug = slug
        self.carousel_id = id
        self.max_items = max_items

    def get_object(self, context):
        """
        Retrieves the object from the database according to the context.
        """
        def prepare_string_field(value):
            if value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            else:  # a template variable was given
                value = template.Variable(value).resolve(context)
            return value

        obj, name, slug, id = self.carousel_object, self.carousel_name, self.carousel_slug, self.carousel_id
        
        if obj is not None:
            return template.Variable(obj).resolve(context)

        if slug is not None:
            return Carousel.objects.get(slug=prepare_string_field(slug))

        if name is not None:
            return Carousel.objects.get(name=prepare_string_field(name))
        
        try:
            id = int(id)
        except ValueError:
            id = template.Variable(id).resolve(context)
        return Carousel.objects.get(pk=id)
    
    def render(self, context):
        try:
            carousel = self.get_object(context)
        except ObjectDoesNotExist:
            return ''
        
        elements = carousel.get_elements()
        if self.max_items:
            max_items = template.Variable(self.max_items).resolve(context)
            elements = elements[:max_items]
        context['carousel'] = carousel
        context['elements'] = elements
        return render_to_string('carousel/templatetags/carousel.html', context)
