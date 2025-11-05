from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from users.models import User


class AuthForm(AuthenticationForm):
    """
    Форма авторизации
    """

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
