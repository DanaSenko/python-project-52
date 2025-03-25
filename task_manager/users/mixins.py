from django.contrib import messages
from django.shortcuts import redirect


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            messages.error(
                request, "Для редактирования пользователя необходима авторизация."
            )
            return redirect("login")  # Перенаправление на страницу входа

        # Проверяем, пытается ли пользователь редактировать свой профиль
        user_to_edit = self.get_object()
        if user_to_edit != request.user:
            messages.error(request, "У вас нет прав для изменения другого пользователя.")
            return redirect(
                "users_list"
            )  # Перенаправление на страницу списка пользователей

        return super().dispatch(request, *args, **kwargs)
