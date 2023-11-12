from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.urls import reverse


class Species(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField(max_length=100)
    species = models.ForeignKey(
        to=Species, on_delete=models.CASCADE, related_name="breeds"
    )

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    identification_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex="^\d{10}$", message="Enter a valid identification number"
            )
        ],
    )
    home_address = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Client"
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("pets:client-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.first_name + " - " + self.identification_number


class Pet(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    fur_color = models.CharField(max_length=50)
    fur_length = models.CharField(max_length=50)
    sterilized = models.BooleanField(default=False)

    breed = models.ForeignKey(to=Breed, on_delete=models.CASCADE, related_name="pets")
    species = models.ForeignKey(
        to=Species, on_delete=models.CASCADE, related_name="pets"
    )
    owner = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_name="pets")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("pets:pet-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Appointment(models.Model):
    NUTRITION_TYPES = [
        ("homemade", "Homemade"),
        ("balanced", "Balanced"),
        ("barf", "BARF"),
    ]

    pet = models.ForeignKey(
        to=Pet, on_delete=models.CASCADE, related_name="appointments"
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    heart_rate = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=10,
                message="The value can't be less than 10 breaths per minute",
            ),
            MaxValueValidator(
                limit_value=200,
                message="The value can't be more than 200 breaths per minute",
            ),
        ]
    )
    breathing_frequency = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=10,
                message="The value can't be less than 10 beats per minute",
            ),
            MaxValueValidator(
                limit_value=500,
                message="The value ca't be more than 500 beats per minute",
            ),
        ]
    )
    threw_up = models.BooleanField(default=False)
    diarrhea = models.BooleanField(default=False)
    nutrition = models.CharField(max_length=20, choices=NUTRITION_TYPES)
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("pets:appointment-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Appointment for {self.pet.name}"


class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    species = models.ForeignKey(
        to=Species, on_delete=models.CASCADE, related_name="vaccines"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Vaccination(models.Model):
    date = models.DateField()
    next_date = models.DateField()
    vaccine = models.ForeignKey(
        to=Vaccine, on_delete=models.CASCADE, related_name="vaccinations"
    )
    pet = models.ForeignKey(
        to=Pet, on_delete=models.CASCADE, related_name="vaccionations"
    )

    def __str__(self):
        return f"{self.vaccine.name} on {self.pet.name}"
