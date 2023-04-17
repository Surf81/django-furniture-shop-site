from django import template

register = template.Library()

@register.simple_tag()
def characteristics(characts, count=None):


    if count:
        characts = characts[:count]

    return [{"group": charact.group, 
             "title": charact.title if charact.type == 1 else f"{charact.value} {charact.title}"
            }  for charact in characts]