from django import forms
from django.contrib.auth import get_user_model
from .models import Captcha

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required':'請輸入用戶名',
        'max_length':'用戶名長度限制2~20之間!',
        'min_length':'用戶名長度限制2~20之間!'})
    email = forms.EmailField(error_messages={'required':'請輸入電子郵件信箱!',
                                             'invalid':'請傳入一個正確的信箱!'})
    captcha = forms.CharField(max_length=4, min_length=4, error_messages={
        'required': '請輸入驗證碼',
        'max_length': '驗證碼長度限制4!',
        'min_length': '驗證碼長度限制4!'
    })
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('該電子郵件已被註冊')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = Captcha.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('驗證碼和電子郵件不一致!')
        captcha_model.delete()
        return captcha

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '請輸入電子郵件信箱!',
                                             'invalid': '請傳入一個正確的信箱!'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)

