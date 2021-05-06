from django.urls import path, include
from .views import (LoginView, LogoutView, SignUpView, profile_view,
                    profile_update_view, avatar_update_view, users_list_view,
                    answers_request_view, answer_request_delete_view)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('@/<str:username>/', profile_view, name='profile'),
    path('@/<str:username>/update/', profile_update_view, name='profile_update'),
    path('@/<str:username>/update/avatar/',
         avatar_update_view, name='avatar_update'),
    path('get_all_users/', users_list_view, name='users_list'),
    path('answers/requests/', answers_request_view, name='answer_requests'),
    path('answer/request/<int:pk>/delete/',
         answer_request_delete_view, name='answer_request_delete'),
    path('', include('django.contrib.auth.urls')),
]
