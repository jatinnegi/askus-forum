# import all models
from core.models import Answer, Question, AnswerComment, AnswerRequest

# import all forms
from .forms import AnswerForm, QuestionForm

import json
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from itertools import chain


def home_view(request):

    answers = sorted(Answer.objects.all(), key=lambda t: -t.number_of_upvotes)
    question_form = QuestionForm()

    if request.method == 'POST' and request.user.is_authenticated:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            data = question_form.cleaned_data

            content = data['content']
            anonymous = data['anonymous']

            new_question = Question.objects.create(
                author=request.user, content=content, anonymous=anonymous)
            new_question.save()

            question_pk = new_question.pk

            messages.add_message(request, messages.SUCCESS,
                                 "Question created successfully")

            return HttpResponseRedirect(reverse_lazy('core:question', kwargs={'pk': question_pk}))

    context = {
        'answers': answers,
        'question_form': question_form
    }

    return render(request, 'core/home.html', context)


def question_view(request, pk):
    answer_form = AnswerForm()
    question = get_object_or_404(Question, pk=pk)

    # get current users answers
    if request.user.is_authenticated:
        auth_answers_list = question.answers.filter(author=request.user)

        answers_list = sorted(question.answers.filter(
            ~Q(author=request.user)), key=lambda t: -t.number_of_upvotes)

        answers = chain(auth_answers_list, answers_list)

    else:
        answers = question.answers.all()

    context = {
        'form': answer_form,
        'question': question,
        'answers': answers
    }

    return render(request, 'core/question.html', context)


@login_required
def question_update_view(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.author != request.user:
        return HttpResponseRedirect('core:home')

    form = QuestionForm(instance=question)

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            anonymous = form.cleaned_data['anonymous']

            question.content = content
            question.anonymous = anonymous

            question.save()

            messages.add_message(request, messages.SUCCESS,
                                 "Question edited successfully")

            return HttpResponseRedirect(reverse_lazy('core:question', kwargs={'pk': pk}))

    context = {'question_form': form}

    return render(request, 'core/question_update.html', context)


@login_required
def question_delete_view(request, pk):
    question = get_object_or_404(Question, pk=pk)

    response = JsonResponse({}, safe=False)

    if question.author == request.user:
        question.delete()
        response.status_code = 200

        messages.add_message(request, messages.SUCCESS,
                             "Question deleted successfully")

        return response

    response.status_code = 400

    return response


@ login_required
def answer_view(request, pk):

    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)

        content = data['content']
        anonymous = data['anonymous']

        if content.__len__() == 0:
            response = JsonResponse({}, safe=False)
            response.status_code = 400
            return response

        answer = Answer.objects.create(
            question=question, author=request.user, content=content, anonymous=anonymous)

        answer.save()

        messages.add_message(request, messages.SUCCESS,
                             "Answer added successfully")

        response = JsonResponse({}, safe=False)
        response.status_code = 201

        return response

    return HttpResponseRedirect(reverse_lazy('core:question', kwargs={'pk': pk}))


@login_required
def question_vote_view(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

        if action == 'upvote':
            if request.user in question.downvotes.all():
                question.downvotes.remove(request.user)
                question.upvotes.add(request.user)

            elif request.user in question.upvotes.all():
                question.upvotes.remove(request.user)
            else:
                question.upvotes.add(request.user)

        elif action == 'downvote':
            if request.user in question.upvotes.all():
                question.upvotes.remove(request.user)
                question.downvotes.add(request.user)

            elif request.user in question.downvotes.all():
                question.downvotes.remove(request.user)

            else:
                question.downvotes.add(request.user)

        else:
            pass

        question.save()

        if request.user in question.upvotes.all():
            current_vote = 'upvote'
        elif request.user in question.downvotes.all():
            current_vote = 'downvote'
        else:
            current_vote = 'none'

        return JsonResponse({
            'upvotes': question.upvotes.all().count(),
            'downvotes': question.downvotes.all().count(),
            'current_vote': current_vote
        }, safe=False)


@login_required
def answer_vote_view(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

        if action == 'upvote':
            if request.user in answer.downvotes.all():
                answer.downvotes.remove(request.user)
                answer.upvotes.add(request.user)

            elif request.user in answer.upvotes.all():
                answer.upvotes.remove(request.user)
            else:
                answer.upvotes.add(request.user)

        elif action == 'downvote':
            if request.user in answer.upvotes.all():
                answer.upvotes.remove(request.user)
                answer.downvotes.add(request.user)

            elif request.user in answer.downvotes.all():
                answer.downvotes.remove(request.user)

            else:
                answer.downvotes.add(request.user)

        else:
            pass

        answer.save()

        if request.user in answer.upvotes.all():
            current_vote = 'upvote'
        elif request.user in answer.downvotes.all():
            current_vote = 'downvote'
        else:
            current_vote = 'none'

        return JsonResponse({
            'upvotes': answer.upvotes.all().count(),
            'downvotes': answer.downvotes.all().count(),
            'current_vote': current_vote
        }, safe=False)


@login_required
def comment_view(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)
        comment = data['comment']

        answer_comment = AnswerComment.objects.create(
            answer=answer, user=request.user, content=comment)
        answer_comment.save()

        response = JsonResponse({
            'id': answer_comment.pk,
            'answer_id': answer_comment.answer.pk,
            'user': {
                'username': answer_comment.user.username,
                'avatar': answer_comment.user.get_avatar,
            },
            'content': answer_comment.content,
            'upvotes': answer_comment.upvotes.all().count(),
            'downvotes': answer_comment.downvotes.all().count(),
            'uploaded_on': answer_comment.uploaded_on
        }, safe=False)

        response.status_code = 201

        return response


@login_required
def comment_vote_view(request, pk):
    comment = get_object_or_404(AnswerComment, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

        if action == 'upvote':
            if request.user in comment.downvotes.all():
                comment.downvotes.remove(request.user)
                comment.upvotes.add(request.user)

            elif request.user in comment.upvotes.all():
                comment.upvotes.remove(request.user)
            else:
                comment.upvotes.add(request.user)

        elif action == 'downvote':
            if request.user in comment.upvotes.all():
                comment.upvotes.remove(request.user)
                comment.downvotes.add(request.user)

            elif request.user in comment.downvotes.all():
                comment.downvotes.remove(request.user)

            else:
                comment.downvotes.add(request.user)

        else:
            pass

        comment.save()

        if request.user in comment.upvotes.all():
            current_vote = 'upvote'
        elif request.user in comment.downvotes.all():
            current_vote = 'downvote'
        else:
            current_vote = 'none'

        return JsonResponse({
            'upvotes': comment.upvotes.all().count(),
            'downvotes': comment.downvotes.all().count(),
            'current_vote': current_vote
        }, safe=False)


@login_required
def answer_update_view(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question = Question.objects.get(pk=answer.question.pk)

    if request.user != answer.author:
        return HttpResponseRedirect(reverse_lazy('core:home'))

    form = AnswerForm(instance=answer)

    context = {
        'question': question,
        'form': form
    }

    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            anonymous = form.cleaned_data['anonymous']

            if content.__len__() == 0:
                return HttpResponseRedirect(reverse_lazy('core:answer_update', kwargs={'pk': pk}))

            answer.content = content
            answer.anonymous = anonymous

            answer.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Answer updated successfully!')
            return HttpResponseRedirect(reverse_lazy('core:question', kwargs={'pk': question.pk}))

    return render(request, 'core/answer_update.html', context)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(AnswerComment, pk=pk)

    if request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()

            response = JsonResponse({}, safe=False)
            response.status_code = 200

            return response


@login_required
def answer_delete_view(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.method == 'DELETE':
        if request.user == answer.author:
            answer.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Answer deleted successfully!")

            response = JsonResponse({}, safe=False)
            response.status_code = 200

            return response

    return JsonResponse({}, safe=False)


@login_required
def question_request_view(request, pk):
    User = get_user_model()
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)
        users_list = data['users_list']
        new_request = AnswerRequest()

        new_request.user = request.user
        new_request.question = question

        new_request.save()

        for user in users_list:
            pk = User.objects.get(username=user).pk
            new_request.request_list.add(pk)

        new_request.save()

        messages.add_message(request, messages.SUCCESS,
                             "Answer requests sent successfully!")

        response = JsonResponse({}, safe=False)
        response.status_code = 201

        return response


@login_required
def answer_share_view(request, pk):

    answer = Answer.objects.get(pk=pk)

    if request.method == 'POST':
        success_message = ""
        if request.user in answer.shares.all():
            answer.shares.remove(request.user)
            success_message = "Answer unshared!"
        else:
            answer.shares.add(request.user)
            success_message = "Answer shared!"

        answer.save()
        messages.add_message(request, messages.SUCCESS, success_message)

        return HttpResponseRedirect(reverse_lazy('core:question', kwargs={'pk': answer.question.pk}))

    return HttpResponseRedirect(reverse_lazy('core:question', kwargs={'pk': answer.question.pk}))


def search_view(request):
    query = request.GET.get('q')

    if query == None or query == '':
        return HttpResponseRedirect(reverse_lazy('core:home'))

    questions = Question.objects.filter(Q(content__icontains=query))
    answers = set()
    questions_set = set()

    for question in questions:
        answer = question.answers.all().order_by('upvotes').first()

        if answer == None:
            questions_set.add(question)
        else:
            answers.add(answer)

    context = {
        'query': query,
        'questions': questions_set,
        'answers': answers
    }

    return render(request, 'core/search.html', context)
