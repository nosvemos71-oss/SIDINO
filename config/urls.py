
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

login_view = auth_views.LoginView.as_view(
    template_name="registration/login.html",
    redirect_authenticated_user=False,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Gestión personalizada de usuarios
    path(
        "dashboard/rector/usuarios/",
        include("apps.users.urls"),
    ),
    path("academics/", include("apps.academics.urls")),

    # Rutas principales de SIDINO
    path("", include("apps.core.urls")),
]
