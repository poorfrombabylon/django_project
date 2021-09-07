from django.http import HttpResponseRedirect, HttpResponse
from .forms import NewUserForm
from django.views import generic

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class NUView(generic.CreateView):
    form_class = NewUserForm
    template_name = 'registration/new.html'
    success_url = '/user/login'

    def form_valid(self, form):
        valid = super(NUView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email_address = form.cleaned_data.get('email_address')
        return valid

