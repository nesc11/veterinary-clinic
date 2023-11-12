from django.contrib import admin
from .models import Species, Breed, Pet, Client, Vaccine

# Register your models here.
admin.site.register(Species)
admin.site.register(Breed)
admin.site.register(Pet)
admin.site.register(Client)
admin.site.register(Vaccine)
