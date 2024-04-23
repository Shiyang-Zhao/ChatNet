from django.shortcuts import render

def home(request):
    # Render the template for the start page
    return render(request, 'home.html')  # Render 'home.html' as the start page
