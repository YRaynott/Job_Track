from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string, random
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Captcha
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def authlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登入
                login(request, user)
                # 是否需要記住我
                if remember:
                    # 沒有要記住的話要設定過期時間
                    request.session.set_expiry(0)
                # 否則使用默認的2周過期時間
                return redirect('/track')
            else:
                print("email帳號或密碼錯誤!")
                # 以下可以用來回傳form在html作錯誤呈現
                #form.add_error('email', 'email帳號或密碼錯誤!')
                #return render(request, 'login.html', context={'form': form})
                return redirect(reverse('jobauth:login'))

@require_http_methods(['GET','POST'])
def authregister(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 用create_user會加密password
            User.objects.create_user(username=username, email=email, password=password)
            # 成功創建之後跳轉到登入頁面
            return redirect(reverse('jobauth:login'))
        else:
            print(form.errors)
            # 創建失敗重新註冊
            return redirect(reverse('jobauth:register'))
            #return render(request, 'register.html', {'form': form})

def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': '必須傳電子郵件帳號'})

    # 生成驗證碼(4位數字)
    captcha = "".join(random.sample(string.digits, 4))

    # update_or_create:原本存在就更新，否則創建
    Captcha.objects.update_or_create(email=email, defaults={'captcha': captcha})

    # 設定發送驗證碼時的名稱，避免使用者找不到
    from_email = '求職追蹤APP 驗證中心 <dev.test.ver@gmail.com>'

    # send_mail("求職追蹤APP註冊驗證碼", message=f"您的註冊驗證碼是: {captcha}。請在3分鐘之內完成註冊!",
    #           recipient_list=[email], from_email=from_email)

    # 主旨與內容
    subject = "求職追蹤APP註冊驗證碼"
    to = [email]
    text_content = f"您的註冊驗證碼是: {captcha}"

    # 渲染 HTML 模板
    html_content = render_to_string('email.html', {'code': captcha})

    # 寄送郵件
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return JsonResponse({'code': 200, 'message': '電子郵件驗證碼發送成功!'})

def authlogout(request):
    logout(request)
    return redirect('/auth/login')