from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from research.forms import AuthForm
from users.decorators import user_has_access


class LoginView(BaseLoginView):
    form_class = AuthForm
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("research:index")


@method_decorator(user_has_access, "dispatch")
class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(reverse_lazy("research:login"))


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class IndexView(generic.TemplateView):
    template_name = "index.html"
