from django.shortcuts import render, redirect
from accounts.admin import UserCreationForm


# Create your views here.
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "accounts/register.html", {"form": form})
