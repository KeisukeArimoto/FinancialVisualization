from django.shortcuts import render, redirect
from django.contrib.auth import logout

from visualizeData import APP_LABEL


def Home(request):
    if request.method == 'GET':
        return render(request, '%s/home.html' % APP_LABEL)
    elif request.method == 'POST':
        if request.POST['action'] == 'myinformation':
            # TODO 自分の情報管理ページへ移動
            pass
        if request.POST['action'] == 'logout':
            logout(request)
            return redirect('/login')
        return render(request, '%s/home.html' % APP_LABEL)
