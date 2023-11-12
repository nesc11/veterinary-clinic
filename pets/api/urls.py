from django.urls import path
from . import views


app_name = "pets_api"


urlpatterns = [
    path("appointments/", views.AppointmentList.as_view(), name="appointment-list"),
    path("appointments/<int:pk>/", views.AppointmentDetail.as_view(),
         name="appointment-detail"),
    path("pets/", views.PetList.as_view(), name="pet-list"),
    path("pets/<int:pk>/", views.PetDetail.as_view(),
         name="pet-detail"),
]
