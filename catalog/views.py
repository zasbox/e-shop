from django.shortcuts import render


# Create your views here.

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name}, {phone}, {message}')
    return render(request, 'home.html')


def contacts(request):

    return render(request, 'contacts.html')
