from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class MathModel(models.Model):
    name = models.CharField(
        verbose_name="Название объекта исследования", max_length=255
    )
    a_0 = models.FloatField(verbose_name="Значение коэффициента a0")
    a_1 = models.FloatField(verbose_name="Значение коэффициента a1")
    a_2 = models.FloatField(verbose_name="Значение коэффициента a2")
    a_3 = models.FloatField(verbose_name="Значение коэффициента a3")
    a_4 = models.FloatField(verbose_name="Значение коэффициента a4")
    a_5 = models.FloatField(verbose_name="Значение коэффициента a5")
    a_6 = models.FloatField(verbose_name="Значение коэффициента a6")
    a_7 = models.FloatField(verbose_name="Значение коэффициента a7")
    a_8 = models.FloatField(verbose_name="Значение коэффициента a8")

    class Meta:
        verbose_name = "Математическая модель"
        verbose_name_plural = "Математические модели"

    def __str__(self):
        return self.name


class Experiment(models.Model):
    math_model = models.ForeignKey(
        MathModel,
        verbose_name="Математическая модель",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name="Дата проведения", auto_now_add=True)
    t_min = models.FloatField(
        verbose_name="Нижний порог температуры спекания в С",
        validators=[MinValueValidator(-273)],
    )
    t_max = models.FloatField(verbose_name="Верхний порог температуры спекания в С")
    delta_t = models.FloatField(
        verbose_name="Шаг варьирования  температуры спекания в С",
        validators=[MinValueValidator(-273)],
    )
    tau_min = models.FloatField(
        verbose_name="Нижний порог времени изометрической выдержки в минутах",
        validators=[MinValueValidator(0)],
    )
    tau_max = models.FloatField(
        verbose_name="Верхний порог времени изометрической выдержки в минутах",
        validators=[MinValueValidator(0)],
    )
    delta_tau = models.FloatField(
        verbose_name="Шаг варьирования времени изометрической выдержки в минутах",
        validators=[MinValueValidator(0)],
    )
    results = models.JSONField(
        verbose_name="Результаты эксперимента", null=True, blank=True, default=list
    )

    class Meta:
        verbose_name = "Эксперимент"
        verbose_name_plural = "Эксперименты"

    def __str__(self):
        return f"Эксперимент No{self.id}"

    def clean(self):
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def calculate(self):
        a_0 = self.math_model.a_0
        a_1 = self.math_model.a_1
        a_2 = self.math_model.a_2
        a_3 = self.math_model.a_3
        a_4 = self.math_model.a_4
        a_5 = self.math_model.a_5
        a_6 = self.math_model.a_6
        a_7 = self.math_model.a_7
        a_8 = self.math_model.a_8

        def polynom_calculate(t, tau):
            return (
                a_0
                + a_1 * t
                + a_2 * tau
                + a_3 * t * tau
                + a_4 * t**2
                + a_5 * tau**2
                + a_6 * t**2 * tau
                + a_7 * t * tau**2
                + a_8 * t**2 * tau**2
            )

        result_tmin_const = {}
        result_tmax_const = {}
        result_tavg_const = {}
        tavg = (self.t_min + self.t_max) / 2

        tau = self.tau_min
        while tau <= self.tau_max:
            result_tmin_const[tau] = polynom_calculate(self.t_min, tau)
            result_tmax_const[tau] = polynom_calculate(self.t_max, tau)
            result_tavg_const[tau] = polynom_calculate(tavg, tau)
            tau += self.delta_tau

        result_taumin_const = {}
        result_taumax_const = {}
        result_taumavg_const = {}

        tauavg = (self.tau_min + self.tau_max) / 2

        t = self.t_min
        while t <= self.t_max:
            result_taumin_const[t] = polynom_calculate(t, self.tau_min)
            result_taumax_const[t] = polynom_calculate(t, self.tau_max)
            result_taumavg_const[t] = polynom_calculate(t, tauavg)
            t += self.delta_t

        self.results = {
            "result_tmin_const": result_tmin_const,
            "result_tmax_const": result_tmax_const,
            "result_tavg_const": result_tavg_const,
            "result_taumin_const": result_taumin_const,
            "result_taumax_const": result_taumax_const,
            "result_taumavg_const": result_taumavg_const,
        }
        self.save()
