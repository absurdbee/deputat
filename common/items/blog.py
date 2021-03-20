def linebreaks(value, autoescape=None):
    from django.utils.html import linebreaks
    from django.utils.safestring import mark_safe
    autoescape = autoescape and not isinstance(value, SafeData)
    return mark_safe(linebreaks(value, autoescape))


def get_blog(user, value):
    from blog.models import Blog

    block = ''

    return ''.join([block, 'blog'])
