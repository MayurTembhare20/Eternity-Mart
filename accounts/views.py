from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import (UserAuthenticationForm,
                    UserRegistrationForm,
                    UserForm,
                    UserProfileForm              
                   )

from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View


class Login_View(View):
    """ Create Login View """
    form_class = UserAuthenticationForm
    template_name = 'accounts/login.html'

    def get(self, request):
        next_url = request.GET.get('next')
        form = self.form_class(initial={
            'next_url' : next_url
        })
        context ={
            'form' : form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = form.cleaned_data.get('next_url')
            if next_url:
                return redirect(next_url)
            messages.success(request,'Succesfullly Login')
            return redirect('home_page')
        else:
            messages.error(request,'Credential Error')
            
        context = {
            'form' : form,
        }
        return render(request, self.template_name, context)


@login_required
def logout_view(request):
    """ Create Logout View """
    logout(request)
    messages.success(request,'Succesfullly Logout')
    return redirect('home_page')


class Register_View(View):
    """ Create Register View """
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form' : form
        }       
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('LoginView')
        context = {
            'form' : form,
        }
        messages.success(request,'Succesfullly Register')
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class Profile_View(View):
    """ User Profile View """
    form_class = UserForm
    profile_form_class = UserProfileForm
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        user = User.objects.get(id = request.user.id)
        user_form = self.form_class(instance = user)
        user_profile_form = self.profile_form_class(instance = user.user_profile)
        context = {
            'user_form' : user_form,
            'user_profile_form' : user_profile_form,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
            form =PasswordChangeForm(request.user,request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request,user)
                messages.success(request,'Your password was succesfully updated!')
                return redirect('Profile_View')
            else:
                messages.error(request,'Please correct the error below')
        else:
            form = PasswordChangeForm(request.user)

        user = User.objects.get(id = request.user.id)
        user_form = self.form_class(request.POST, instance = user)
        user_profile_form = self.profile_form_class(request.POST, instance = user.user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()

        context = {
            'user_form' : user_form,
            'user_profile_form' : user_profile_form,
            'form': form
        }
        return render(request, self.template_name, context)
