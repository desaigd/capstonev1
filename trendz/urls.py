from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
  

    # API Routes
    path("chart", views.chart, name="chart"),
    path("normalval", views.normalval, name="normalval"),
    path("deleterecord", views.deleterecord, name="deleterecord")
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)