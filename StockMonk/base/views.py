from django.shortcuts import render

def home(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'aboutpage.html')

def contact(request):
    return render(request, 'contactpage.html')

def trial(request):
    return render(request, 'trialpage.html')

def demo(request):
    return render(request, 'demopage.html')