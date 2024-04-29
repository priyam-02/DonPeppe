from django.urls import path, include

from . import views
from .views import GeneratePdf

urlpatterns = [
    path('hed2/', views.hed2),
    path('',views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('showcart/', views.showcart),
    path('cart/', views.cart),
    path('removecart/<int:id>/', views.removecart),
    path('checkout/', views.checkout),
    path('pd/<int:id>/', views.pd),
    path('menu/<int:id>/', views.menu),
    path('menuf/', views.menuf),
    path('menuc/<int:id>/', views.menuc),
    path('forgotapp/', views.forgot),
    path('resetpw/', views.resetpw),
    path('service/', views.service),
    path('team/', views.team),
    path('history/', views.history),
    path('booktable/', views.booktable),
    path('bookt2/', views.bookt2),
    path('thankyou/', views.thankyou),
    path('contact/', views.contact),
    path('checkout/', views.checkout),
    path('pdf/', GeneratePdf.as_view()),
    path('payments/', views.payments),
]