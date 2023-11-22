from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q



# Create your views here.

def store(request, category_slug=None):
    categories  =None
    products    =None
    
    if category_slug !=None:
        categories      = get_object_or_404(Category, slug=category_slug)
        products        = Product.objects.filter(category=categories, is_available=True)
        paginator       = Paginator(products, 4)
        page            = request.GET.get('page')
        paged_products  = paginator.get_page(page)
        product_count   = products.count()
    else:
        products        = Product.objects.all().filter(is_available=True).order_by('id')
        paginator       = Paginator(products, 6)
        page            = request.GET.get('page')
        paged_products  = paginator.get_page(page)
        
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product   = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart          = CartItem.objects.filter(cart__cart_id=_cart_id(request), product = single_product).exists()
    
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)
""" 
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {'products': products }
    return render(request, 'store/store.html', context)
"""

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Define the fields you want to search
            searchable_fields = [
                'product_name',
                'product_description',
                'compatible_devices',
                'installation_type',
                'color',
                'brand',
                'storage_capacity',
                'hard_disk_interface',
                'special_feature',
            ]

            # Initialize an empty Q object to aggregate all queries
            q_objects = Q()

            # Construct OR queries for each searchable field
            for field in searchable_fields:
                q_objects |= Q(**{f"{field}__icontains": keyword})

            # Filter products based on the aggregated queries
            products = Product.objects.filter(q_objects).order_by('-created_date')

    context = {'products': products }
    return render(request, 'store/store.html', context)
