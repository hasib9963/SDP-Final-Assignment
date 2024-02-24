from django.urls import path
from . import views
urlpatterns = [

    path('add/', views.AddPetCreateView.as_view(), name='add_pet'),
    path('edit/<int:id>/', views.EditPetView.as_view(), name='edit_pet'),
    path('delete/<int:id>/', views.DeletePetView.as_view(), name='delete_pet'),
    path('details/<int:id>/', views.DetailPetView.as_view(), name='detail_pet'),
    path('details/<int:id>/post-review/', views.DetailPetView.as_view(), name='post_review'),
]
