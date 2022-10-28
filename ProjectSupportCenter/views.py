from django.shortcuts import render
from django.db.models import Q


def aboutUs(request):
    return render(request, 'about.html')


