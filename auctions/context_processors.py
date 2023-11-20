
from .models import Category

def categories(request):
    return {'categories': Category.objects.all()}


def category_info(request):
    is_categories = request.path.startswith('/category/')
    return {'is_categories': is_categories}