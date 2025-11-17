from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
import psutil
import os


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
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self):
        return self.name


class Experiment(models.Model):
    material = models.ForeignKey(
        MathModel,
        verbose_name="Материал",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name="Дата проведения", auto_now_add=True)
    t_min = models.FloatField(
        verbose_name="Нижний порог температуры спекания в С",
        validators=[MinValueValidator(-273)],
    )
    t_max = models.FloatField(
        verbose_name="Верхний порог температуры спекания в С",
        validators=[MinValueValidator(-273)],
    )
    t_avg = models.FloatField(
        verbose_name="Средняя температура спекания в С", default=0
    )
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
    tau_avg = models.FloatField(
        verbose_name="Среднее время изометрической выдержки в минутах", default=0
    )
    delta_tau = models.FloatField(
        verbose_name="Шаг варьирования времени изометрической выдержки в минутах",
        validators=[MinValueValidator(0)],
    )
    results = models.JSONField(
        verbose_name="Результаты эксперимента", null=True, blank=True, default=list
    )
    calculation_time = models.FloatField(default=0, verbose_name="Время расчета")
    number_of_math_operations = models.IntegerField(
        default=0, verbose_name="Количество математических операций"
    )
    memory_used = models.FloatField(
        default=0, verbose_name="Затрачено оперативной памяти"
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
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024
        start_time = datetime.now()
        a_0 = self.material.a_0
        a_1 = self.material.a_1
        a_2 = self.material.a_2
        a_3 = self.material.a_3
        a_4 = self.material.a_4
        a_5 = self.material.a_5
        a_6 = self.material.a_6
        a_7 = self.material.a_7
        a_8 = self.material.a_8

        number_of_math_operations = 0

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

        result_t_const = {}
        self.t_avg = (self.t_min + self.t_max) / 2

        number_of_math_operations += 1

        tau = self.tau_min
        while tau <= self.tau_max:
            result_t_const[tau] = {
                "tmin_const": None,
                "tmax_const": None,
                "tavg_const": None,
            }
            result_t_const[tau]["tmin_const"] = round(
                polynom_calculate(self.t_min, tau), 4
            )
            result_t_const[tau]["tmax_const"] = round(
                polynom_calculate(self.t_max, tau), 4
            )
            result_t_const[tau]["tavg_const"] = round(
                polynom_calculate(self.t_avg, tau), 4
            )
            tau += self.delta_tau
            number_of_math_operations += 79
        result_tau_const = {}

        self.tau_avg = (self.tau_min + self.tau_max) / 2
        number_of_math_operations += 1
        t = self.t_min
        while t <= self.t_max:
            result_tau_const[t] = {
                "taumin_const": None,
                "taumax_const": None,
                "tauavg_const": None,
            }
            result_tau_const[t]["taumin_const"] = round(
                polynom_calculate(t, self.tau_min), 4
            )
            result_tau_const[t]["taumax_const"] = round(
                polynom_calculate(t, self.tau_max), 4
            )
            result_tau_const[t]["tauavg_const"] = round(
                polynom_calculate(t, self.tau_avg), 4
            )
            t += self.delta_t
            number_of_math_operations += 79
        self.results = {
            "result_t_const": result_t_const,
            "result_tau_const": result_tau_const,
        }
        memory_after = process.memory_info().rss / 1024
        self.memory_used = round(memory_after - memory_before, 4)
        end_time = datetime.now()
        calctime = round((end_time.timestamp() - start_time.timestamp()) * 1000, 2)
        self.calculation_time = calctime
        self.number_of_math_operations = number_of_math_operations
        self.save()
