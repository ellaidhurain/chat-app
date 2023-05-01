from django.shortcuts import render

# Create your views here.


def index(request, *args, **kwargs):
    # context={
    #     'firstname':'ellaidhurai',
    #     "lastname":"ed"
    # }
    return render(request, 'frontend/index.html')
