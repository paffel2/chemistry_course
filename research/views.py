from math import e
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages


from research.forms import AuthForm, ExperimentForm
from research.models import Experiment
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


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class ExperimentCreateView(generic.FormView):
    template_name = "experiment_form.html"
    form_class = ExperimentForm
    success_url = reverse_lazy("research:experiment_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            experiment = form.save()
            experiment.calculate()
            messages.success(self.request, "Эксперимент успешно проведен!")
            return redirect("research:experiment_results", pk=experiment.id)
        else:
            messages.error(self.request, "Эксперимент успешно не проведен!")
            print(form.errors)
            return self.form_invalid(form)


"""
    def form_valid(self, form):
        experiment = form.save()
        try:
            experiment.calculate()
            messages.success(self.request, "Эксперимент успешно проведен!")
            return redirect("research:experiment_results", pk=experiment.id)

        except Exception as e:
            experiment.delete()
            messages.error(
                self.request, f"Ошибка при проведении эксперимента: {str(e)}"
            )
            print("HERE1")
            return self.form_invalid(form)
"""


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class ExperimentResultsView(generic.DetailView):
    model = Experiment
    template_name = "experiment_results.html"
    context_object_name = "experiment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment = self.get_object()
        if experiment.results:
            context["experiment_results"] = str(experiment.results)
        return context


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class ExperimentListView(generic.ListView):
    model = Experiment
    template_name = "experiment_list.html"
    context_object_name = "experiments"
    ordering = ["-created_at"]
    paginate_by = 10
