from django.shortcuts import render
from django.urls import path, include

from modules.users.views import LoginView, ResetView, ForgotView, LogoutView, ProfileView, CreateView, ListUserView, \
    UserRemoveView, ActivateView, UserEditView, RangRemoveView, RangsCreateView, ListRangView, RangEditView, \
    UserProfileView, AvatarChangeView

urlpatterns = (
    path('login/', LoginView.as_view(), name="user_login_view"),
    path('logout/', LogoutView.as_view(), name='user_logout_view'),
    path('reset/<uidb64>/<token>/', ResetView.as_view(), name="user_reset_view"),
    path('forgot/', ForgotView.as_view(), name="user_forgot_view"),
    path('profile/', ProfileView.as_view(), name="profile_view"),
    path('create/', CreateView.as_view(), name="user_create_view"),
    path('list/', ListUserView.as_view(), name="user_list_view"),
    path('edit/<int:pk>/', UserEditView.as_view(), name="user_edit_view"),
    path('remove/<int:pk>/', UserRemoveView.as_view(), name="user_remove_view"),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="user_activate_view"),
    path('rang/create/', RangsCreateView.as_view(), name="rang_create_view"),
    path('rang/remove<int:pk>', RangRemoveView.as_view(), name="rang_remove_view"),
    path('rang/list', ListRangView.as_view(), name="rang_list_view"),
    path('rang/edit/<int:pk>/', RangEditView.as_view(), name="rang_edit_view"),
    path('profil/<str:username>/', UserProfileView.as_view(), name="user_profile_view"),
    path('change/', AvatarChangeView.as_view(), name="user_avatar_change_view"),
)

