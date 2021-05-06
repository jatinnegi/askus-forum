from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('question/<int:pk>/', views.question_view, name='question'),
    path('question/<int:pk>/vote/', views.question_vote_view, name='question_vote'),
    path('question/<int:pk>/edit/',
         views.question_update_view, name='question_update'),
    path('question/<int:pk>/delete/',
         views.question_delete_view, name='question_delete'),
    path('question/<int:pk>/requests/', views.question_request_view,
         name='question_request'),
    path('answer/<int:pk>/', views.answer_view, name='answer'),
    path('answer/<int:pk>/vote/', views.answer_vote_view, name='answer_vote'),
    path('answer/<int:pk>/edit/', views.answer_update_view, name='answer_update'),
    path('answer/<int:pk>/delete/', views.answer_delete_view, name='answer_delete'),
    path('answer/<int:pk>/comment/', views.comment_view, name='comment'),
    path('answer/<int:pk>/share/', views.answer_share_view, name='answer_share'),
    path('comment/<int:pk>/vote/', views.comment_vote_view, name='comment_vote'),
    path('comment/<int:pk>/delete/',
         views.comment_delete_view, name='comment_delete'),
    path('search/', views.search_view, name='search'),
]
