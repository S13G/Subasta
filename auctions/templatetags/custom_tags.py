from django import template

register = template.Library()


@register.simple_tag
def watchlist_count(request):
    # access user by passing request as a parameter and as argument in the template
    owner = request.user
    watchlist_item_count = owner.item.filter(watchlist=True).count()
    return watchlist_item_count
