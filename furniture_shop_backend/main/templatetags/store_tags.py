from django import template

register = template.Library()

@register.simple_tag()
def characteristics(characts, count=None):


    if count:
        characts = characts[:count]

    return [{"group": charact.group, 
             "title": charact.title if charact.type == 1 else f"{charact.value} {charact.title}"
            }  for charact in characts]


@register.inclusion_tag("main/.inc/favorite.html", takes_context=True)
def favorite_widget(context, item, href="", favorite_class=""):
    is_visible = False
    is_favorite = False

    if (user := context.get('user')) and user.is_authenticated:
        is_visible = True
        is_favorite = item.favorite

    options = {
        'visible': is_visible,
        'href': href,
        'is_favorite': is_favorite,
        'class': favorite_class,
    }
    return {'favorite': options}