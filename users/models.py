from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import CustomUserManager


class User(AbstractUser):
    name = models.CharField(verbose_name="ФИО", max_length=255)
    email = models.EmailField(verbose_name="Email", unique=True)
    password = models.CharField(verbose_name="Пароль", max_length=255)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    is_superuser = models.BooleanField(
        verbose_name="Статус суперпользователя (администратора)", default=False
    )
    is_staff = models.BooleanField(
        verbose_name="Статус сотрудника (исследователя)", default=False
    )
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    username = None
    groups = None
    user_permissions = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
