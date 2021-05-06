from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import views, authenticate, login
from django.contrib import messages
from django.views.generic import CreateView
from .forms import LoginForm, SignUpForm, AvatarUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
import os
from core.models import Question


class LoginView(views.LoginView):
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('core:home'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = super(LoginView, self).get_success_url()

        messages.add_message(self.request, messages.SUCCESS,
                             "Logged in successfully")

        return url


class LogoutView(views.LogoutView):
    def get_next_page(self):
        next_page = super(LogoutView, self).get_next_page()

        messages.add_message(self.request, messages.SUCCESS,
                             "Logged out successfully")

        return next_page


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('core:home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('core:home'))

        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)

        messages.add_message(self.request, messages.SUCCESS,
                             'Your profile was created successfully')

        return HttpResponseRedirect(self.success_url)


def profile_view(request, username):
    User = get_user_model()

    try:
        user = User.objects.get(username=username)
        form = AvatarUpdateForm()
        context = {
            'profile_user': user,
            'form': form
        }
        return render(request, 'registration/profile.html', context)
    except User.DoesNotExist:
        return render(request, '404.html', {'msg': 'No user found'})


@login_required
def avatar_update_view(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    if user == request.user:
        if request.method == 'POST':
            form = AvatarUpdateForm(request.POST, request.FILES)

            if form.is_valid():
                avatar = form.cleaned_data['avatar']

                if user.avatar:
                    user.avatar.delete()

                user.avatar = avatar
                user.save()

                messages.add_message(request, messages.SUCCESS,
                                     "Avatar updated successfully!")

                return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': username}))

    return HttpResponseRedirect(reverse_lazy('accounts:profile', kwargs={'username': username}))


@login_required
def profile_update_view(request, username):
    User = get_user_model()

    user = get_object_or_404(User, username=username)

    if user == request.user:
        if request.method == 'POST':
            data = json.loads(request.body)
            first_name = user.first_name
            last_name = user.last_name
            bio = user.bio

            try:
                first_name = data['first_name']
            except KeyError:
                pass

            try:
                last_name = data['last_name']
            except KeyError:
                pass

            try:
                bio = data['bio']
            except KeyError:
                pass

            user.first_name = first_name
            user.last_name = last_name
            user.bio = bio

            user.save()

            response = JsonResponse({
                'first_name': first_name,
                'last_name': last_name,
                'bio': bio,
            }, safe=False)

            response.status_code = 200

            return response

    return JsonResponse({}, safe=False)


def users_list_view(request):
    User = get_user_model()
    all_users = User.objects.filter(~Q(pk=request.user.pk))
    users_list = []

    for user in all_users:

        user_dict = {
            'avatar': user.get_avatar,
            'username': user.username,
            'answers': user.answers.all().count(),
        }
        users_list.append(user_dict)

    response = JsonResponse({
        'users': users_list
    }, safe=False)
    response.status_code = 200

    return response


@login_required
def answers_request_view(request):

    all_requests = request.user.answer_requests.all()

    data = []

    for answer_request in all_requests:
        question_id = answer_request.question.pk
        answered = False

        question = Question.objects.get(pk=question_id)

        try:
            if request.user.answers.get(question=question):
                answered = True
        except:
            pass

        data.append({
            'answer_request_id': answer_request.pk,
            'question_id': question_id,
            'username': answer_request.user.username,
            'content': answer_request.question.content,
            'answered': answered
        })

    response = JsonResponse(data, safe=False)

    return response


@login_required
def answer_request_delete_view(request, pk):

    try:
        answer_request = request.user.answer_requests.get(pk=pk)
        answer_request.request_list.remove(request.user.pk)
        answer_request.save()
    except:
        response = JsonResponse({}, safe=False)
        response.status_code = 400
        return response

    response = JsonResponse({}, safe=False)
    response.status = 200

    return response
