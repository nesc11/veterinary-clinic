from .models import Species


def species(request):
    species = Species.objects.all()
    return {
        "species": species
    }
