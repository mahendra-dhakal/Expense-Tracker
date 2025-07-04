from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import  UserLoginView, UserRegisterView, ExpenseIncomeView

router=DefaultRouter()

router.register(r'expenses', ExpenseIncomeView, basename='expense')

urlpatterns=[
    path('',include(router.urls)),
    path('auth/register/', UserRegisterView, name='register'),
    path('auth/login/',UserLoginView, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(),name='token_refresh')

]