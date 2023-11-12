from rest_framework import generics
from pets.models import Appointment, Pet
from pets.api.serializers import AppointmentSerializer, PetSerializer


class AppointmentList(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDetail(generics.RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class PetList(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


class PetDetail(generics.RetrieveAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
