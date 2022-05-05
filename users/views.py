from django.shortcuts import redirect, render
from django.views import View
from users.models import CustomUser
from users.forms import UserCreationForm,UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class RegisterView(View):
    def get(self, request):
        create_form = UserCreationForm()
        context = {
            'form': create_form,
        }
        return render(request, 'register.html', context)
    def post(self, request): 
        create_form = UserCreationForm(data=request.POST,
                                       files=request.FILES
                                       )
        if create_form.is_valid():
            create_form.save()
            
            return redirect('users:login')
        else:
            context = {
                'form': create_form,
            }
            return render(request, 'register.html', context)
            
            
            
            
class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'login.html', {'login_form': login_form})
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            messages.success(request, 'You have successfully logged in!')
            return redirect('books:list')
        else:
            return render(request, 'login.html', {'login_form': login_form})
        
class ProfileView(LoginRequiredMixin,View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return render(request, 'profile.html', {'user': request.user})
    
class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out!')
        return redirect('index')
    
class ProfileUpdateView(LoginRequiredMixin,View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        return render(request, 'profile_edit.html', {'form': user_update_form})
    def post(self, request):
        user_update_form = UserUpdateForm(data=request.POST,
                                          instance=request.user,
                                          files=request.FILES
                                          )
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
        else:
            return render(request, 'profile_edit.html', {'form': user_update_form})