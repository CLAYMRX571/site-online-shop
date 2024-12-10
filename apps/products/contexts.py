from .models import Category

def get_categories(request):
    parent_categories = Category.objects.filter(is_active=True, level=0)
    context =  {
        'categories': parent_categories
    }
    return context