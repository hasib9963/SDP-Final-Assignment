from django.urls import path
from .views import DepositMoneyView, AdoptPetView, PetReportView


# app_name = 'transactions'
urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("adopt/<int:pet_id>/", AdoptPetView.as_view(), name="adopt_pet"),
    path('report/', PetReportView.as_view(), name='report'),
]