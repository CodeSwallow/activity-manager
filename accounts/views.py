from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from accounts.forms import SignUpForm


class SignUpView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super(SignUpView, self).form_valid(form)
