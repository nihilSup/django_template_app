'contains custom template tags'
from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/ctgs.html')
def get_category_list(ctg=None):
    'returns dict woth ctg list available by key: ctgs'
    return {
        'ctgs': Category.objects.all(),
        'act_ctg': ctg
    }
