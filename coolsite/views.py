import form as form
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import *
from .models import User

class Index(ListView):
    template_name = 'index.html'
    model = Posts

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "Вам отправлены инкструкции по восстановлению на указанный email, " \
                      "Если аккаунт с таким email существует, инструкции будут получены в ближайшее время" \
                      " Если вы не получили письмо, " \
                      "Пожалуйста убедитесь, что email коректен и проверьте папку Спам."
    success_url = reverse_lazy('home-page')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Ваш пароль успешно изменён"
    success_url = reverse_lazy('home-page')

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обнвовлён')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

class CreatePostView(CreateView):
    form_class = CreatePostForm
    template_name = 'addpost.html'
    success_url = reverse_lazy('home-page')

class ShowPost(DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'

@login_required
def enemy_page(request, id):
    cur_user = id
    data = {
        'name': User.objects.get(pk=cur_user).username
    }
    return render(request, 'profile.html', data)

def find_friends(id):
    fr = Friend.objects.all()
    friends_array = []
    fr1 = Friend.objects.filter(friend1=id)
    fr2 = Friend.objects.filter(friend2=id)
    for f in fr1:
        friends_array.append(f.friend2.id)
    for f in fr2:
        friends_array.append(f.friend1.id)
    return friends_array

def friends(request):
    cur_user = request.user
    fr = Friend.objects.all()
    friends_array = find_friends(cur_user.id)
    friends_names = []

    for i in friends_array:
        friends_names.append((User.objects.get(pk=i).username,i))

    for i in friends_names:
        print(i)
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():

            uzver = form.cleaned_data['user']

            will_add = User.objects.get(username=uzver)

            if find_friends(will_add.id).count(cur_user.id) == 0 and will_add.id != cur_user.id:
                a = Friend(friend1=Profile.objects.get(pk=cur_user.pk), friend2=Profile.objects.get(pk=will_add.pk))
                a.save()
            return redirect('friends')
        else:
            error = "Форма была неверной"

    form = RequestForm(request.POST)

    data = {
        'friends': friends_names,
        'form':form,

    }

    return render(request, 'friends.html',data)








