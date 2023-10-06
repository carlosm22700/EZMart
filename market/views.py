from django.shortcuts import render

# Controllers/Views go here


def home(request):
    return render(request, 'home.html')


def fetch_sheet_data():
    pass
