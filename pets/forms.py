from django import forms
from .models import Breed, Pet, Appointment, Client, Vaccination, Species, Vaccine


class PetForm(forms.ModelForm):
    # breed = forms.ModelChoiceField(
    #     queryset=Breed.objects.filter(species__name=animal_kind))

    def __init__(self, animal_kind=None, *args, **kwargs):
        self.animal_kind = animal_kind
        super().__init__(*args, **kwargs)
        self.fields["breed"].queryset = Breed.objects.filter(species__name=animal_kind)
        for field in self.fields:
            if field == "sterilized":
                self.fields[field].widget.attrs["class"] = "form-check-input"
            elif field in ["owner", "breed"]:
                self.fields[field].widget.attrs["class"] = "form-select"
                self.fields[field].empty_label = self.fields[field].label
            else:
                self.fields[field].widget.attrs["placeholder"] = self.fields[
                    field
                ].label
                self.fields[field].widget.attrs["class"] = "form-control"

    class Meta:
        model = Pet
        exclude = ["species", "created", "updated"]
        widgets = {"birthdate": forms.widgets.DateInput(attrs={"type": "date"})}


class ClientForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs["class"] = "form-control"
    #         self.fields[field].widget.attrs["placeholder"] = self.fields[field].label

    class Meta:
        model = Client
        fields = "__all__"


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ["threw_up", "diarrhea"]:
                self.fields[field].widget.attrs["class"] = "form-check-input"
            elif field == "nutrition":
                self.fields[field].widget.attrs["class"] = "form-select"
                self.fields[field].choices = [
                    ("", "Select a nutrition type...")
                ] + self.fields[field].choices[1:]

            else:
                self.fields[field].widget.attrs["placeholder"] = self.fields[
                    field
                ].label
                self.fields[field].widget.attrs["class"] = "form-control"
                if field == "reason":
                    self.fields[field].widget.attrs["rows"] = "3"
                    self.fields[field].widget.attrs[
                        "placeholder"
                    ] = "This appointment was booked because..."

    class Meta:
        model = Appointment
        exclude = ["created", "updated", "pet"]
        labels = {
            "temperature": "Temperature(°F)",
            "weight": "Weight (kg)",
            "heart_rate": "Heart rate (bpm)",
            "breathing_frequency": "Breathing frequency (breaths/min)",
        }


class VaccinationForm(forms.ModelForm):
    def __init__(self, *args, species_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["vaccine"].queryset = Vaccine.objects.filter(
            species__name=species_name
        )

    class Meta:
        model = Vaccination
        fields = ["vaccine", "date", "next_date"]
        widgets = {
            "date": forms.widgets.DateInput(attrs={"type": "date"}),
            "next_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }
