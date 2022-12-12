from django.urls import path, include
from rest_framework import routers

from app.views import PrinterViewSet, CheckViewSet, create_check, orders, print_check

router = routers.DefaultRouter()

router.register("printers", PrinterViewSet)
router.register("checks", CheckViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("orders/", orders, name='orders'),
    path("create-check/", create_check, name='create-check'),
    path("print-check/", print_check, name='print-check'),
]

app_name = "app"
