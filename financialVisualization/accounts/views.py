from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from accounts import APP_LABEL


def Login(request):
    if request.method == 'GET':
        return render(request, '%s/login.html' % APP_LABEL)
    elif request.method == 'POST':
        EMAIL = request.POST['email_address']
        PASS = request.POST['password']

        # Djangoの認証機能
        print(EMAIL)
        print(PASS)
        user = authenticate(username=EMAIL, password=PASS)
        print(user)

        # ユーザ認証
        if user:
            # ユーザアクティベート判定
            if user.is_active:
                login(request, user)
                # ホーム画面遷移
                return render(request, '%s/#' % APP_LABEL)
            else:
                # ユーザアクティベートしていないときの処理
                return render(request, '%s/login.html' % APP_LABEL)
        else:
            # メールアドレスまたはパスワードに不備がある
            return render(request, '%s/login.html' % APP_LABEL)
    return render(request, '%s/login.html' % APP_LABEL)


@login_required
def Logout(request):
    logout(request)
    return render(request, '%s/login.html' % APP_LABEL)


def register(request):
    return render(request, '%s/register.html' % APP_LABEL)


def set_password(request):
    return render(request, '%s/password.html' % APP_LABEL)
