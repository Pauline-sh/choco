from django.shortcuts import render, get_object_or_404
from choco.models import Assortment


def home_page(request):
    chocos = Assortment.objects.all()
    return render(request, 'home.html', {'chocos': chocos})
