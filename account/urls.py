from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/support/", views.support_page, name="support_page"),

    path("", views.account, name="account"),
    path("kyc-reg/", views.kyc_registration, name="kyc-reg"),

]