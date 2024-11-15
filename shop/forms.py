from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import Review


class RegisterUserForm(UserCreationForm):
    """Форма реєстрації користувачів"""
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}), min_length=8,
                                error_messages={'min_length': 'Пароль повинен бути довжиною не менше 8 символів'})
    password2 = forms.CharField(label='Повтор паролю', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Паролі не співпадають')
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Пароль повинен містити не менше 8 символів.')
        if password1.isdigit():
            raise forms.ValidationError('Пароль повинен містити хоча б один символ, крім цифр.')
        return password1

    class Meta:
        model = User  # пов'язуємо форму з вбудованою моделлю User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """Форма для автентифікації користувачів"""
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FeedbackForm(forms.Form):
    """Форма зворотного зв'язку"""
    name = forms.CharField(label='Ім’я', max_length=100)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Повідомлення', widget=forms.Textarea(attrs={'cols': 30, 'rows': 4}))
    capatcha = CaptchaField(label='Введіть капчу з картинки')


class ReviewForm(forms.ModelForm):
    """Форма для залишення відгуку на товар"""

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control shadow px-2',
                       'rows': 6
                       }
            ),
            'rating': forms.RadioSelect
        }
