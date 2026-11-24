from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin as DjangoPermissionRequiredMixin,
)


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Restringe una vista basada en clases a determinados roles.
    """

    allowed_roles = ()
    raise_exception = True

    def test_func(self):

        user = self.request.user

        if user.is_superuser:
            return True

        return user.groups.filter(
            name__in=self.allowed_roles
        ).exists()


class PermissionRequiredMixin(
    LoginRequiredMixin,
    DjangoPermissionRequiredMixin,
):
    """
    Restringe una vista basada en clases a un permiso Django.
    """

    raise_exception = True