from django.http import HttpResponse


def ss(request):
    return HttpResponse("Hello, world. You're at the polls index.")