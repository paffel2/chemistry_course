from django.urls import path

from research.views import (
    LoginView,
    LogoutView,
    IndexView,
    ExperimentCreateView,
    ExperimentResultsView,
    ExperimentListView,
    ExperimentRecalculateView,
    export_experiment_to_excel,
)

app_name = "research"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", IndexView.as_view(), name="index"),
    path("create/", ExperimentCreateView.as_view(), name="experiment_create"),
    path(
        "results/<int:pk>/",
        ExperimentResultsView.as_view(),
        name="experiment_results",
    ),
    path("list/", ExperimentListView.as_view(), name="experiment_list"),
    path(
        "results/<int:pk>/recalculate/",
        ExperimentRecalculateView.as_view(),
        name="experiment_recalculate",
    ),
    path(
        "results/<int:pk>/export-excel/",
        export_experiment_to_excel,
        name="experiment_export_excel",
    ),
]
