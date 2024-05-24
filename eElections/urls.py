from django.contrib import admin
from django.urls import include, path, re_path


from base.views import (home, signup, logout, CustomLoginView, CustomPasswordResetView, CustomPasswordResetDoneView,
                        CustomPasswordResetConfirmView, CustomPasswordResetCompleteView)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),

    path("accounts/signup/", signup, name="signup"),
    path("accounts/logout/", logout, name='logout'),
    path('captcha/', include('captcha.urls')),

    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path("accounts/password_reset/", CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='custom_password_reset_confirm'),
    path('accounts/reset/done', CustomPasswordResetCompleteView.as_view(), name='custom_password_reset_complete'),

    path('accounts/', include('django.contrib.auth.urls')),

]
