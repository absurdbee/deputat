from django import template
import pymorphy2
from string import ascii_letters
from elect.models import SubscribeElect
register=template.Library()


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False

@register.filter
def rupluralize(value, arg="единица,единицы,единиц"):
    args = arg.split(",")
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


@register.filter
def is_elect_subscribe(user, elect):
    if SubscribeElect.is_elect_subscribe(elect.pk, user.pk):
        return True
    else:
        return False
