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
from financialVisualization.settings_local import EMAIL_HOST_USER, HOST
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
            context = {'error_messages': e.messages}
            return render(request, '%s/login.html' % APP_LABEL, context)

        user = authenticate(username=EMAIL, password=PASS)

        if user:
            if user.is_active:
                login(request, user)
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
    # TODO ログアウトした後、すぐにログインできない (別ページに移動して、再度ログインページに入るとできる)事象解消
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
            pass
        else:
            CustomUser.objects.create_nomal_user(
                email=email, password=None, active=False)

        send_register_mail(email)
        context = {
            'success_messages': ['パスワード登録用のメールを送信しました。', 'メール記載のリンクよりパスワードを登録してください。']}
        return render(request, '%s/register.html' % APP_LABEL, context)
    return render(request, '%s/register.html' % APP_LABEL)


def send_register_mail(email):
    subject = '登録用メール'
    recipient_list = [email]
    from_mail = EMAIL_HOST_USER

    payload_data = {'email': email}
    tokenGenerator = TokenGenerator()
    token = tokenGenerator.generateToken(payload_data=payload_data)
    host = HOST
    url = f"http://{host}/login/password/{token}"
    print(url)

    # TODO メール文言修正
    msg_html = render_to_string('mails/register_mail.html', {'url': url})
    msg_txt = render_to_string('mails/register_mail.txt')

    send_mail(subject, msg_txt, from_mail,
              recipient_list, html_message=msg_html)


def set_password(request, token):
    if request.method == 'GET':
        return render(request, '%s/password.html' % APP_LABEL)
    elif request.method == 'POST':
        tokenGenerator = TokenGenerator()
        payload = tokenGenerator.decodeToken(token)
        email = payload.get('email')
        user = CustomUser.objects.get(email=email)
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
                context = {'error_messages': e.messages}
                return render(request, '%s/password.html' % APP_LABEL, context)

            CustomUser.objects.change_password(email, PASS, True)

            context = {'success_messagess': ['パスワードを登録しました。早速ログインしてみましょう！']}
            return render(request, '%s/password.html' % APP_LABEL, context)

        else:
            context = {'error_messages': ['リンクが不正です。再度メールアドレスの登録からやり直してください']}
            return render(request, '%s/password.html' % APP_LABEL, context)
    return render(request, '%s/password.html' % APP_LABEL)
