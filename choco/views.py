from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Assortment
from .cart import Cart
from .forms import CartAddProductForm

context = {'cart_quantity': 1}
def home_page(request):
    return render(request, 'home.html', context)


def about_page(request):
    return render(request, 'about.html', context)


def contacts_page(request):
    return render(request, 'contacts.html', context)


def details_page(request, pk):
    choco_item = get_object_or_404(Assortment, pk=pk)
    context['item'] = choco_item
    return render(request, 'details.html', context)


def catalog_page(request):
    chocos_list = Assortment.objects.all()

    paginator = Paginator(chocos_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        chocos = paginator.page(page)
    except PageNotAnInteger:
        chocos = paginator.page(1)
    except EmptyPage:
        chocos = paginator.page(paginator.num_pages)

    context['chocos'] = chocos
    return render(request, 'catalog.html', context)


def cart_page(request):
    return render(request, 'cart.html', context)


def cart_add(request, pk):
    pass


def cart_remove(request, pk):
    pass


"""
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')
 
 
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
 
 
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
"""
