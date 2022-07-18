from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from bookshop.models import CustomerOrder, Review


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ['mail', 'city', 'post_department', 'phone_number']


class RegistrationUserForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=25, label='Логін')
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(), label='пароль')
    password_confirm = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(), label='пароль')
    email = forms.EmailField(required=True, label='електронна пошта')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('зареєструватися', 'Зареєструватися'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def clean_password_confirm(self):
        password_one = self.cleaned_data.get('password')
        password_two = self.cleaned_data.get('password_confirm')
        password_has_num = [True for sym in password_one if sym.isdigit()]

        if password_one != password_two:
            raise forms.ValidationError('Паролі не співпадають')
        if len(password_one) < 8:
            raise forms.ValidationError('Пароль має бути довше 8 символів')
        if not password_one[0].isalpha():
            raise forms.ValidationError('Перший символ у паролі має бути великою літерою')
        if not password_one[0].isupper():
            raise forms.ValidationError('Перший символ у паролі має бути великою літерою')
        if not sum(password_has_num) > 0:
            raise forms.ValidationError('Пароль повинен містити хоча б одне число')

        return password_two

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check_mail = User.objects.filter(email=email)

        if len(check_mail) > 0:
            raise forms.ValidationError('Ця електронна адреса вже використовується')

        return email


class LoginUserForm(forms.Form):
    username = forms.CharField(required=True, max_length=25, label='Логін')
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(), label='Пароль')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('увійти', 'Увійти'))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        check_username = User.objects.filter(username=username)

        if not len(check_username):
            raise forms.ValidationError('Користувача с таким логіном не знайдено')

        check_password = authenticate(username=username, password=password)

        if check_password is None:
            raise forms.ValidationError('Неправильний пароль')

        return self.cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'body', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('залишити рецензiю', 'Залишити рецензiю'))
