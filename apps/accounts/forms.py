from django import forms
from .models import User, PasswordResetCode
from apps.common.utils import get_random_string_code

class RegisterUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=True)

    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email oldin ro'yxatdan o'tgan")
        return email
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Parollar bir xil emas!!!")
        
        return password2

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        user = super().save(commit)
        user.set_password(password)
        user.save()
        return user

class LoginForm(forms.Form):
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        if not phone or not password:
            raise forms.ValidationError("Bo'sh bo'lish kerak emas!!!")
        return self.cleaned_data
    
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'photo', 'phone', 'address')

class UpdatePasswordForm(forms.ModelForm):
    password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('password', )

    def clean_password(self):
        old_pass = self.cleaned_data.get('password')
        if not self.instance.check_password(old_pass):
            raise forms.ValidationError("Eski parol xato!!!")
        return old_pass

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Parolda kamchilik bor!!")
        return password2  

    def save(self, commit=True):
        password = self.cleaned_data.get('confirm_password')
        self.instance.set_password(password)
        self.instance.save()
        return self.instance  

class PasswordResetForm(forms.ModelForm):
    email = forms.EmailField( required=True)
    
    class Meta:
        model = PasswordResetCode
        fields = ('email',)
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError("Bu email bazada mavjud emas")
        return email
    
    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        code = get_random_string_code()
        code = PasswordResetCode.objects.create(email = email, code = code)
        return code
    
class ResetNewPasswordForm(forms.Form):
    password = forms.CharField( required=True)
    confirm_password = forms.CharField( required=True)
    
    
    def clean_confirm_password(self):   
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Parollar bir biriga mos emas!!!")

        return password2