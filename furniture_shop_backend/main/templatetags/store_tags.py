from django import template

register = template.Library()

@register.inclusion_tag("main/.inc/characteristics_as_ul.html", takes_context=False)
def characteristics_as_ul(characts, count=None):
    if count:
        characts = characts[:count]

    to_public = list()
    for charact in characts:
        if charact.type == 1:
            title = charact.title 
        else:
            if hasattr(charact, 'value'):
                title = f"{charact.value} {charact.title}"
            else:
                title = f"- {charact.title}"
        to_public.append({
            "group": charact.group, 
            "title": title
        })

    return {'characteristics': {
        'list': to_public
    }}


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