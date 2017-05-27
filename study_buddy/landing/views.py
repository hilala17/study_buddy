from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'landing/home.html', context)
    
def about(request):
    context = {}
    return render(request, 'landing/about.html', context)
    
def chat(request):
    context = {}
    return render(request, 'landing/chat.html', context)
    
def settings(request):
    context = {}
    return render(request, 'landing/settings.html', context)
    
def settings_classes(request):
    context = {}
    return render(request, 'landing/settings_classes.html', context)
    
def connections(request):
    context = {}
    return render(request, 'landing/connections.html', context)