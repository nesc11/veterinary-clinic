from rest_framework import serializers
from pets.models import Appointment, Pet, Breed, Species


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "appointments"]
