from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def SalamView(request):
    return render(request, 'home_page.html')
