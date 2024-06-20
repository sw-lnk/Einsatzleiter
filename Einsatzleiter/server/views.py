from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return redirect('mission_dashboard')
    return render(request, "base_generic.html", {})