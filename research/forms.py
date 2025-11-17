import math
from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from django import forms
from .models import Experiment, MathModel
from django.core.exceptions import ValidationError


class AuthForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "label": "Логин",
                "placeholder": "Введите логин",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "label": "Пароль",
                "placeholder": "Введите пароль",
            }
        )

    def get_invalid_login_error(self):
        return ValidationError("Неверный имя пользователя или пароль")

    def clean(self):
        super().clean()
        username = self.cleaned_data.get("username")
        user = User.objects.filter(email=username).first()
        if user and not user.is_can_access:
            self.add_error(None, "Нет прав для входа")
        return self.cleaned_data


class ExperimentForm(forms.ModelForm):

    material = forms.ModelChoiceField(
        queryset=MathModel.objects.all(),
        label="Материал",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    t_min = forms.FloatField(
        label="Нижний порог температуры спекания (°C)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=1300,
    )

    t_max = forms.FloatField(
        label="Верхний порог температуры спекания (°C)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=1550,
    )

    delta_t = forms.FloatField(
        label="Шаг варьирования температуры спекания (°C)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=10,
    )

    tau_min = forms.FloatField(
        label="Нижний порог времени изометрической выдержки (мин)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=30,
    )

    tau_max = forms.FloatField(
        label="Верхний порог времени изометрической выдержки (мин)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=60,
    )

    delta_tau = forms.FloatField(
        label="Шаг варьирования времени изометрической выдержки (мин)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        initial=2,
    )

    class Meta:
        model = Experiment
        fields = [
            "material",
            "t_min",
            "t_max",
            "delta_t",
            "tau_min",
            "tau_max",
            "delta_tau",
        ]

    def clean(self):
        cleaned_data = super().clean()

        t_min = cleaned_data.get("t_min")
        t_max = cleaned_data.get("t_max")
        delta_t = cleaned_data.get("delta_t")
        tau_min = cleaned_data.get("tau_min")
        tau_max = cleaned_data.get("tau_max")
        delta_tau = cleaned_data.get("delta_tau")

        errors = {}

        if t_min is not None and t_max is not None and t_min > t_max:
            errors["t_min"] = (
                "Нижний порог температуры спекания должен быть меньше верхнего."
            )

        if tau_min is not None and tau_max is not None and tau_min > tau_max:
            errors["tau_min"] = (
                "Нижний порог времени изометрической выдержки должен быть меньше верхнего."
            )

        if delta_t is not None and delta_t <= 0:
            errors["delta_t"] = (
                "Шаг варьирования температуры спекания должен быть больше нуля."
            )

        if delta_tau is not None and delta_tau <= 0:
            errors["delta_tau"] = (
                "Шаг варьирования времени изометрической выдержки должен быть больше нуля."
            )

        if t_min is not None and t_max is not None and delta_t is not None:
            if (t_max - t_min) / delta_t > 1000:
                errors["delta_t"] = (
                    "Слишком маленький шаг температуры. Увеличьте шаг или уменьшите диапазон."
                )

        if tau_min is not None and tau_max is not None and delta_tau is not None:
            if (tau_max - tau_min) / delta_tau > 1000:
                errors["delta_tau"] = (
                    "Слишком маленький шаг времени. Увеличьте шаг или уменьшите диапазон."
                )
        if errors:
            raise ValidationError(errors)

        return cleaned_data
