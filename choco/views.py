from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Assortment
from .cart import Cart
from .forms import CartAddProductForm

def home_page(request):
    return render(request, 'home.html')


def about_page(request):
    return render(request, 'about.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def details_page(request, pk):
    choco_item = get_object_or_404(Assortment, pk=pk)
    cart_form = CartAddProductForm()

    return render(request, 'details.html', {'item': choco_item, 'cart_form': cart_form})


def catalog_page(request):
    chocos_list = Assortment.objects.all()

    paginator = Paginator(chocos_list, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        chocos = paginator.page(page)
    except PageNotAnInteger:
        chocos = paginator.page(1)
    except EmptyPage:
        chocos = paginator.page(paginator.num_pages)

    return render(request, 'catalog.html', {'chocos': chocos})


def cart_page(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart.html', {'cart': cart})


def cart_add(request, pk):
    cart = Cart(request)
    choco_item = get_object_or_404(Assortment, pk=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=choco_item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('choco:cart')


def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Assortment, pk=pk)
    cart.remove(product)
    return redirect('choco:cart')
