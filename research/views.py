from math import e
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
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
            return self.form_invalid(form)


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class ExperimentResultsView(generic.DetailView):
    model = Experiment
    template_name = "experiment_detail.html"
    context_object_name = "experiment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experiment = self.get_object()
        if experiment.results:
            context["experiment_results"] = str(experiment.results)
            context["chart_data"] = self.prepare_chart_data(experiment.results)
        return context

    def prepare_chart_data(self, results):
        """Подготавливает данные для графиков Chart.js"""
        chart_data = {}
        if "result_t_const" in results:
            chart_data["constant_temp"] = {
                "labels": list(results["result_t_const"].keys()),
            }
            data_tmin = []
            data_tmax = []
            data_tavg = []
            for obj in results["result_t_const"].values():
                data_tmin.append(obj["tmin_const"])
                data_tmax.append(obj["tmax_const"])
                data_tavg.append(obj["tavg_const"])

            chart_data["constant_temp"]["datasets"] = [
                {
                    "label": f"Tемпература = {self.object.t_min}°C",
                    "data": data_tmin,
                    "borderColor": "#ff6384",
                    "backgroundColor": "rgba(255, 99, 132, 0.1)",
                    "tension": 0.4,
                },
                {
                    "label": f"Tемпература = {self.object.t_max}°C",
                    "data": data_tmax,
                    "borderColor": "#36a2eb",
                    "backgroundColor": "rgba(54, 162, 235, 0.1)",
                    "tension": 0.4,
                },
                {
                    "label": f"Tемпература = {(self.object.t_min + self.object.t_max) / 2}°C",
                    "data": data_tavg,
                    "borderColor": "#4bc0c0",
                    "backgroundColor": "rgba(75, 192, 192, 0.1)",
                    "tension": 0.4,
                },
            ]

        if "result_tau_const" in results:
            chart_data["constant_time"] = {
                "labels": list(results["result_tau_const"].keys())
            }
            data_taumin = []
            data_taumax = []
            data_tauavg = []
            for obj in results["result_tau_const"].values():
                data_taumin.append(obj["taumin_const"])
                data_taumax.append(obj["taumax_const"])
                data_tauavg.append(obj["tauavg_const"])

            chart_data["constant_time"]["datasets"] = [
                {
                    "label": f"Время = {self.object.tau_min} мин",
                    "data": data_taumin,
                    "borderColor": "#ff9f40",
                    "backgroundColor": "rgba(255, 159, 64, 0.1)",
                    "tension": 0.4,
                },
                {
                    "label": f"Время = {self.object.tau_max} мин",
                    "data": data_taumax,
                    "borderColor": "#9966ff",
                    "backgroundColor": "rgba(153, 102, 255, 0.1)",
                    "tension": 0.4,
                },
                {
                    "label": f"Время = {(self.object.tau_min + self.object.tau_max) / 2} мин",
                    "data": data_tauavg,
                    "borderColor": "#ffcd56",
                    "backgroundColor": "rgba(255, 205, 86, 0.1)",
                    "tension": 0.4,
                },
            ]

        return chart_data


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class ExperimentListView(generic.ListView):
    model = Experiment
    template_name = "experiment_list.html"
    context_object_name = "experiments"
    ordering = ["-created_at"]
    paginate_by = 10


@method_decorator(user_has_access, "dispatch")
@method_decorator(never_cache, "dispatch")
class ExperimentRecalculateView(generic.View):
    def post(self, request, pk):
        experiment = get_object_or_404(Experiment, pk=pk)

        try:
            experiment.calculate()
            experiment.save()
            messages.success(request, "Результаты эксперимента успешно пересчитаны!")
        except Exception as e:
            messages.error(request, f"Ошибка при пересчете: {str(e)}")

        return redirect("research:experiment_results", pk=experiment.id)
