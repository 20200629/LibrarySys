from django import template
from django.db.models.aggregates import Count
from ..models import Book,Tag
from users.models import User
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_recent_books(num=6):
    return Book.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_books=Count('book')).filter(num_books__gt=0)

@register.simple_tag
def get_recent_tags(num=6):
    return Tag.objects.all()[:num]





