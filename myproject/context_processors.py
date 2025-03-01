from myapp.models import Categories

def category_menu(request):
    return {
        "menucategories": Categories.objects.filter(showinmenu=True).order_by("-name")
    }
