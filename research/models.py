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
        if self.t_min > self.t_max:
            raise ValidationError(
                "Нижний порог температуры спекания должен быть меньше верхнего."
            )
        if self.tau_min > self.tau_max:
            raise ValidationError(
                "Нижний порог времени изометрической выдержки должен быть меньше верхнего."
            )
        if self.delta_t <= 0:
            raise ValidationError(
                "Шаг варьирования  температуры спекания должен быть больше нуля."
            )
        if self.delta_tau <= 0:
            raise ValidationError(
                "Шаг варьирования времени изометрической выдержки должен быть больше нуля."
            )
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
