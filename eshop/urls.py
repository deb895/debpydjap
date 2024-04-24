from django.contrib import admin
from django.urls import path,include


from . import views

from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register('',views.RegistrationViewSet )


urlpatterns = [

    path("",views.index,name = "home" ), 
    path("registration", views.registrationform, name="registration"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("cart",views.cartdetails,name="cart"),
    path("checkout",views.checkout_details,name="checkout"),
    path("order",views.order_detail,name="order"),
    path('rest_api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)