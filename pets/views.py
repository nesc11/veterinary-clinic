from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import VaccinationForm
from .models import Species, Pet, Appointment, Breed, Client, Vaccination


from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)


# CLIENT VIEWS
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = "clients"
    paginate_by = 10


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = "__all__"


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    context_object_name = "client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = Pet.objects.filter(owner=self.kwargs["pk"])
        paginator = Paginator(pets, 10)
        page_number = self.request.GET.get("page", 1)
        try:
            pets = paginator.page(page_number)
        except PageNotAnInteger:
            pets = paginator.page(1)
        except EmptyPage:
            pets = paginator.page(paginator.num_pages)

        is_paginated = False
        if paginator.num_pages > 1:
            is_paginated = True

        context["pets"] = pets
        context["is_paginated"] = is_paginated

        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = "__all__"


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client


# PET VIEWS
class PetListView(LoginRequiredMixin, ListView):
    context_object_name = "pets"
    paginate_by = 10

    def get_queryset(self):
        queryset = Pet.objects.all()
        search = self.request.GET.get("search")
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    fields = [
        "breed",
        "name",
        "birthdate",
        "fur_color",
        "fur_length",
        "sterilized",
        "owner",
    ]

    def form_valid(self, form):
        species = get_object_or_404(Species, name=self.kwargs["species_name"])
        form.instance.species = species
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        species = get_object_or_404(Species, name=self.kwargs["species_name"])
        breeds = Breed.objects.filter(species=species)
        form.fields["breed"].queryset = breeds
        return form


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    context_object_name = "pet"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.filter(pet=self.kwargs["pk"])
        paginator = Paginator(appointments, 10)
        page_number = self.request.GET.get("page", 1)
        try:
            appointments = paginator.page(page_number)
        except PageNotAnInteger:
            appointments = paginator.page(1)
        except EmptyPage:
            appointments = paginator.page(paginator.num_pages)

        is_paginated = False
        if paginator.num_pages > 1:
            is_paginated = True

        context["appointments"] = appointments
        context["is_paginated"] = is_paginated

        return context


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    fields = [
        "breed",
        "name",
        "birthdate",
        "fur_color",
        "fur_length",
        "sterilized",
    ]

    def get_form(self):
        form = super().get_form()
        breeds = Breed.objects.filter(species=self.object.species)
        form.fields["breed"].queryset = breeds
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update_form"] = True
        return context


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    success_url = reverse_lazy("pets:pet-list")


# APPOINTMENT VIEWS
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    fields = [
        "weight",
        "temperature",
        "heart_rate",
        "breathing_frequency",
        "threw_up",
        "diarrhea",
        "nutrition",
        "reason",
    ]

    def form_valid(self, form):
        pet = get_object_or_404(Pet, pk=self.kwargs["pet_pk"])
        form.instance.pet = pet
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        pet = get_object_or_404(Pet, pk=self.kwargs["pet_pk"])
        return form


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    fields = [
        "weight",
        "temperature",
        "heart_rate",
        "breathing_frequency",
        "threw_up",
        "diarrhea",
        "nutrition",
        "reason",
    ]


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment

    def get_object(self, queryset=None):
        appointment = get_object_or_404(Appointment, pk=self.kwargs.get("pk"))
        self.pet = appointment.pet
        return appointment

    def get_success_url(self):
        return reverse("pets:pet-detail", kwargs={"pk": self.pet.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pet"] = self.pet
        return context


# VACCINES
@login_required
def vaccinations_by_pet(request, pet_pk):
    pet = get_object_or_404(Pet, pk=pet_pk)
    vaccinations = Vaccination.objects.filter(pet=pet)
    form = VaccinationForm(species_name=pet.species.name)
    if request.method == "POST":
        print(request.POST)
        form = VaccinationForm(request.POST, species_name=pet.species.name)
        if form.is_valid():
            form = form.save(commit=False)
            form.pet = pet
            form.save()
            return redirect("pets:pet-vaccinations", pet_pk=pet.pk)
        print(form.errors)
    return render(
        request,
        "pets/vaccinations/vaccinations_by_pet.html",
        {"pet": pet, "vaccinations": vaccinations, "form": form},
    )


@require_POST
@login_required
def delete_vaccination(request, pet_pk, vaccination_pk):
    vaccination = get_object_or_404(Vaccination, pk=vaccination_pk, pet=pet_pk)
    vaccination.delete()
    return redirect("pets:pet-vaccinations", pet_pk=pet_pk)


@login_required
def update_vaccination(request, pet_pk, vaccination_pk):
    vaccination = get_object_or_404(Vaccination, pk=vaccination_pk, pet=pet_pk)
    form = VaccinationForm(
        instance=vaccination, species_name=vaccination.pet.species.name
    )
    if request.method == "POST":
        form = VaccinationForm(
            request.POST,
            instance=vaccination,
            species_name=vaccination.pet.species.name,
        )
        if form.is_valid():
            form.save()
            return redirect("pets:pet-vaccinations", pet_pk=vaccination.pet.pk)
    return render(request, "pets/vaccinations/vaccination_form.html", {"form": form})
