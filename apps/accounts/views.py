from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.db.models import Q
from .models import User, PasswordResetCode
from apps.order.models import Order, OrderItem
from .forms import RegisterUserForm, LoginForm, UpdatePasswordForm, UpdateUserForm, PasswordResetForm, ResetNewPasswordForm
from django.contrib import messages
from datetime import datetime
from apps.common.utils import custom_send_mail
# Create your views here.

class UserRegisterView(View):
    form_class = RegisterUserForm

    def get(self, request):
        return render(request, 'accounts/register.html')
        
    def post(self, request):
        user_form = self.form_class(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Tizimdan ro'yxatdan o'tdingiz tabriklayman!!!")
            return redirect('index')
        
        messages.error(request, f"Tizimdan ro'yxatdan xatolik!!! {user_form.errors}")
        return render(request, 'accounts/register.html')
    
class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        user_form = self.form_class(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, phone=user_form.cleaned_data['phone'], password=user_form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                messages.success(request, "Siz tizimga kirdingiz!!!")
                return redirect('index')
            
            messages.error(request, "Login yoki parol noto'g'ri!!!")
            return render(request, 'accounts/login.html')
        
        messages.error(request, user_form.errors)
        return render(request, 'accounts/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class UpdateUserView(View):
    form_class = UpdateUserForm

    def post(self, request):
        user_form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Ma'lumotlaringiz yangilandi!!!")
            return redirect('index')
        
        messages.error(request, user_form.errors)
        return redirect('accounts:orders')

class UpdatePasswordView(View):
    form_class = UpdatePasswordForm
    
    def post(self, request):
        user_form = self.form_class(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Ma'lumotlaringiz yangilandi!!!")
            return redirect('index')
        
        messages.error(request, user_form.errors)
        return redirect('accounts:orders')

class PasswordResetView(View):
    form_class = PasswordResetForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/password_reset_form.html', {'form': form})
    
    def post(self, request):
        email_form = self.form_class(data=request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data.get('email')
            reset_code = email_form.save()
            print("reset_code: ", reset_code)
            
            custom_send_mail(email, reset_code.code)
            messages.success(request, f"<< {email} >> email ga kod yuborildi.")
            return redirect('accounts:check-verify-code', reset_code.uuid)
        
        messages.error(request, email_form.errors)
        return redirect('accounts:password-reset')
                   
class CheckVeryfyCodeView(View):
    def get(self, request, uuid):
        code = PasswordResetCode.objects.filter(Q(uuid=uuid) & Q(is_confirmed=False) & Q(expired_time__gte=datetime.now())).first()
        if code:
            return render(request, 'accounts/password_reset_check_verify_code.html')
        
        messages.error(request, "Kod kiritish muddati o'tgan!!!")
        return redirect('accounts:password-reset')
    
    def post(self, request, uuid):
        user_code = request.POST.get('code')
        code = PasswordResetCode.objects.filter(Q(uuid=uuid) & Q(is_confirmed=False) & Q(expired_time__gte=datetime.now())).first()
        if code:
            if user_code == code.code:
                code.is_confirmed = True
                code.save()
                messages.success(request, "Yangi parol kiriting!!!")
                return redirect('accounts:reset-new-password', code.uuid)
            messages.error(request, "Kod xato!!!")
            return redirect('accounts:check-verify-code', code.uuid)
        
        messages.error(request, "Kod kiritish muddati o'tgan!!!")
        return redirect('accounts:password-reset')

class OrderProfileView(View):
    def get(self, request, *args, **kwargs):
        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        orderitems = OrderItem.objects.filter(order=order)
        context = {
            'orderitems': orderitems,
            'order': order,
        }
        return render(request, 'accounts/profile.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, f"Mahsulotlar buyurtma qilish uchun avval shopdan zakaz qiling!!")
            return redirect('shop')

        data = request.POST

        order, created = Order.objects.get_or_create(user=request.user, status='pending')
        OrderItem.objects.create(order=order, product_size_id=data.get('product_size'), quantity=data.get('quantity'))

        messages.success(request, f"Mahsulotlar buyurtma qilindi!")
        return redirect('accounts:login')
    
class ResetNewPasswordView(View):
    form_class = ResetNewPasswordForm
    def get(self, request, uuid):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'accounts/password_reset_confirm.html', context)
    
    def post(self, request, uuid):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            code = PasswordResetCode.objects.get(uuid=uuid)
            user = User.objects.get(email=code.email)
            user.set_password(form.cleaned_data.get('confirm_password'))
            user.save()
            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi.")
            return render(request, 'accounts/password_reset_complete.html')
        
        messages.error(request, form.errors)
        return redirect('accounts:reset-new-password', uuid)
