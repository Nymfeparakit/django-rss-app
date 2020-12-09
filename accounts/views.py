from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('feeds:today')

    def post(self, request, *args, **kwargs):
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('login')
        return render(request, self.template_name, {'form': f})