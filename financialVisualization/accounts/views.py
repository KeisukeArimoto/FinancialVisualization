from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail

from accounts import APP_LABEL
from accounts.models import CustomUser


def Login(request):
    if request.method == 'GET':
        return render(request, '%s/login.html' % APP_LABEL)
    elif request.method == 'POST':
        EMAIL = request.POST['email_address']
        PASS = request.POST['password']

        # TODO EMAL,PASSのバリデーション

        # Djangoの認証機能
        user = authenticate(username=EMAIL, password=PASS)

        # ユーザ認証
        if user:
            # ユーザアクティベート判定
            if user.is_active:
                login(request, user)
                # ホーム画面遷移
                # TODO ホーム画面作成
                return render(request, '%s/#' % APP_LABEL)
            else:
                # ユーザアクティベートしていないときの処理
                context = {'error_message': '本ユーザは使用できません。再度ユーザ登録をしてください'}
                return render(request, '%s/login.html' % APP_LABEL, context)
        else:
            # メールアドレスまたはパスワードに不備がある
            context = {'error_message': 'メールアドレスまたはパスワードが間違っています'}
            return render(request, '%s/login.html' % APP_LABEL, context)
    return render(request, '%s/login.html' % APP_LABEL)


@login_required
def Logout(request):
    logout(request)
    return render(request, '%s/login.html' % APP_LABEL)


def register(request):
    if request.method == 'GET':
        return render(request, '%s/register.html' % APP_LABEL)
    elif request.method == 'POST':
        email = request.POST['email_address']

        # TODO emailバリデーション

        # TODO emailをユーザ登録する

        send_register_mail(email)
        context = {
            'success_message': 'パスワード登録用のメールを送信しました。メール記載のリンクよりパスワードを登録してください。'}
        return render(request, '%s/register.html' % APP_LABEL, context)
    return render(request, '%s/register.html' % APP_LABEL)


def send_register_mail(email):
    subject = '登録用メール'
    recipient_list = [email]
    # TODO 送信元アドレス、パスワードはDB管理 (暗号化) したい
    from_mail = 'ここに送信元のメールアドレスが来るよ'
    # TODO メッセージ内のURLにトークンを埋め込むなどしたい (password設定用ページにてトークンからemailアドレスが取得できるとベスト)
    # TODO 文言修正
    msg_html = render_to_string('mails/register.html')
    msg_txt = render_to_string('mails/register.txt')

    send_mail(subject=subject, message=msg_txt, from_mail=from_mail,
              recipient_list=recipient_list, html_message=msg_html)


def set_password(request):
    if request.method == 'GET':
        return render(request, '%s/password.html' % APP_LABEL)
    elif request.method == 'POST':
        # TODO どこからかemailを取得する
        #user = CustomUser.objects.filter(email=email)
        # if user:
        PASS = request.POST['password']
        PASS_AGAIN = request.POST['password_again']

        if PASS != PASS_AGAIN:
            context = {'error_message': 'パスワードが一致していません。もう一度パスワードを入力してください。'}
            return render(request, '%s/password.html' % APP_LABEL, context)

        # TODO パスワードバリデーション

        # TODO パスワード保存

        context = {'success_message': 'パスワードを登録しました。早速ログインしてみましょう！'}
        return render(request, '%s/password.html' % APP_LABEL, context)

        # else:
        #context = {'error_message': 'リンクが不正です。再度メールアドレスの登録からやり直してください'}
        # return render(request, '%s/password.html' % APP_LABEL, context)
    return render(request, '%s/password.html' % APP_LABEL)
