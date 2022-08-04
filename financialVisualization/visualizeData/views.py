from django.shortcuts import render

from visualizeData import APP_LABEL


def Home(request):
    if request.method == 'GET':
        return render(request, '%s/home.html' % APP_LABEL)
