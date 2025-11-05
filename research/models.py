from django.db import models


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
