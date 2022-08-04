from django.forms import ValidationError
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.template.loader import render_to_string
from django.core.mail import send_mail
from validate_email import validate_email

from accounts import APP_LABEL
from accounts.models import CustomUser
from utils.token import TokenGenerator


def Login(request):
    if request.method == 'GET':
        return render(request, '%s/login.html' % APP_LABEL)
    elif request.method == 'POST':
        EMAIL = request.POST['email_address']
        PASS = request.POST['password']

        if not (validate_email(EMAIL)):
            context = {'error_messages': ['メールアドレスが不正です。メールアドレスを確認してください。']}
            return render(request, '%s/login.html' % APP_LABEL, context)

        try:
            validate_password(PASS)
        except ValidationError as e:
            # TODO errorメッセージを文字列のlistでcontextに入れたい
            context = {'error_messages': e.error_list}
            return render(request, '%s/login.html' % APP_LABEL, context)

        user = authenticate(username=EMAIL, password=PASS)

        if user:
            if user.is_active:
                login(request, user)
                # TODO ホーム画面作成
                return render(request, 'visualizeData/home.html')
            else:
                context = {'error_messages': [
                    'パスワード登録が完了していません。ユーザ登録画面よりパスワード登録を行ってください']}
                return render(request, '%s/login.html' % APP_LABEL, context)
        else:
            context = {'error_messages': ['メールアドレスまたはパスワードが間違っています']}
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

        if not (validate_email(email)):
            context = {'error_messages': [
                'このメールアドレスは登録できません。メールアドレスを確認してください。']}
            return render(request, '%s/register.html' % APP_LABEL, context)

        user = CustomUser.objects.filter(email=email)
        if user:
            # TODO すでにメールアドレスが登録されている場合
            pass
        else:
            CustomUser.objects.create_nomal_user(
                email=email, password=None, active=False)

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

    payload_data = {'email': email}
    tokenGenerator = TokenGenerator()
    token = tokenGenerator.generateToken(payload_data=payload_data)
    # TODO ホスト名は設定ファイルに切り出す?
    url = 'http://127.0.0.1:8000/login/password/%s' % token
    print(url)

    # TODO メール文言修正
    msg_html = render_to_string('mails/register_mail.html', {'url': url})
    msg_txt = render_to_string('mails/register_mail.txt')

    # send_mail(subject=subject, message=msg_txt, from_mail=from_mail,
    #           recipient_list=recipient_list, html_message=msg_html)


def set_password(request, token):
    if request.method == 'GET':
        return render(request, '%s/password.html' % APP_LABEL)
    elif request.method == 'POST':
        tokenGenerator = TokenGenerator()
        payload = tokenGenerator.decodeToken(token)
        email = payload.get('email')
        user = CustomUser.objects.get(email=email)
        print(type(user))
        if user:
            PASS = request.POST['password']
            PASS_AGAIN = request.POST['password_again']

            if PASS != PASS_AGAIN:
                context = {'error_messages': [
                    'パスワードが一致していません。もう一度パスワードを入力してください。']}
                return render(request, '%s/password.html' % APP_LABEL, context)

            try:
                validate_password(PASS)
            except ValidationError as e:
                # TODO errorメッセージを文字列のlistでcontextに入れたい
                context = {'error_messages': e.error_list}
                return render(request, '%s/password.html' % APP_LABEL, context)

            CustomUser.objects.change_password(email, PASS, True)

            context = {'success_message': 'パスワードを登録しました。早速ログインしてみましょう！'}
            return render(request, '%s/password.html' % APP_LABEL, context)

        else:
            context = {'error_messages': '[リンクが不正です。再度メールアドレスの登録からやり直してください]'}
            return render(request, '%s/password.html' % APP_LABEL, context)
    return render(request, '%s/password.html' % APP_LABEL)
