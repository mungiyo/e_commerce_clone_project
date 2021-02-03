from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Product, Category
from photo.models import Product_photo
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import math
from cart.views import add_cart

# Create your views here.


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    image = get_object_or_404(Product_photo, product=product)
    return render(request, 'shop/product_detail.html', context={'product': product,
                                                                'image': image})


def product_list(request):
    if request.method == "POST":
        add_cart(request, request.POST.get('product_id'))
    page = int(request.GET.get('page', 1))     # 현재 페이지 번호를 가져온다. 없으면 1을 가져온다.
    paginated_by = 3        # 페이지당 노출될 개수
    photos = get_list_or_404(Product_photo)
    total_count = len(photos)
    if paginated_by >= total_count:
        total_page = 1
    else:
        total_page = math.ceil(total_count / paginated_by)
    page_range = range(1, total_page+1)
    start_index = paginated_by * (page - 1)
    end_index = paginated_by * page
    photos = photos[start_index:end_index]
    return render(request, 'shop/product_list.html', {'photos': photos, 'total_page': total_page,
                                                      'page_range': page_range})


def mobile_product_list(request):
    photos = Product_photo.objects.all()
    return render(request, 'shop/mobile_product_list.html', {'photos': photos})


def product_review(request):
    return render(request, 'shop/product_review_list.html')


@csrf_exempt
def product_check(request):
    product_name = request.GET.get('product_name')
    context = {'overlap': product_name}
    return JsonResponse(context)


def mobile_category(request):
    return render(request, 'shop/mobile_category.html')
