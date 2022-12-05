"""wms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from wms_api import views

router = routers.DefaultRouter()
router.register('product', views.ProductView, basename="product")
router.register('package/product', views.PackageView, basename="package/product")
router.register("shipment", views.ShipmentDetailsView, basename="shipment")

urlpatterns = [
    path('admin', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', include(router.urls)),
    path('users/', views.WorkerList.as_view()),
    path('users/<int:pk>/', views.WorkerDetails.as_view()),
    path('shipment-details/<int:pk>/', views.AllPackageInOneShipmentView.as_view()),
    # path('shipment-details/', views.ShipmentDetailsView.as_view()),
    # path('package/', views.PackageView.as_view())
]
