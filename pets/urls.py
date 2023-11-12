from django.urls import path
from . import views


app_name = "pets"

urlpatterns = [
    path("", views.PetListView.as_view(), name="pet-list"),
    # Clients
    path("clients/", views.ClientListView.as_view(), name="client-list"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client-detail"),
    path("clients/create/", views.ClientCreateView.as_view(), name="client-create"),
    path(
        "clients/<int:pk>/update/",
        views.ClientUpdateView.as_view(),
        name="client-update",
    ),
    path(
        "clients/<int:pk>/delete/",
        views.ClientDeleteView.as_view(),
        name="client-delete",
    ),
    # Pets
    path("pets/", views.PetListView.as_view(), name="pet-list"),
    path("pets/<int:pk>/", views.PetDetailView.as_view(), name="pet-detail"),
    path(
        "pets/create/<str:species_name>/",
        views.PetCreateView.as_view(),
        name="pet-create",
    ),
    path(
        "pets/<int:pk>/update/",
        views.PetUpdateView.as_view(),
        name="pet-update",
    ),
    path(
        "pets/<int:pk>/delete/",
        views.PetDeleteView.as_view(),
        name="pet-delete",
    ),
    # Appointments
    path(
        "appointments/<int:pk>/",
        views.AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "appointments/create/pet/<int:pet_pk>/",
        views.AppointmentCreateView.as_view(),
        name="appointment-create",
    ),
    path(
        "appointments/<int:pk>/update/",
        views.AppointmentUpdateView.as_view(),
        name="appointment-update",
    ),
    path(
        "appointments/<int:pk>/delete/",
        views.AppointmentDeleteView.as_view(),
        name="appointment-delete",
    ),
    # Vaccionation by pet
    path(
        "pets/<int:pet_pk>/vaccinations/",
        views.vaccinations_by_pet,
        name="pet-vaccinations",
    ),
    path(
        "pets/<int:pet_pk>/vaccinations/<int:vaccination_pk>/delete/",
        views.delete_vaccination,
        name="pet-vaccinations-delete",
    ),
    path(
        "pets/<int:pet_pk>/vaccinations/<int:vaccination_pk>/update/",
        views.update_vaccination,
        name="pet-vaccinations-update",
    ),
]
