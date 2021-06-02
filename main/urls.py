from django.urls import path
from . import views

urlpatterns = [
    path('registrar', views.registerPage, name='register'),
    path('logout', views.logoutPage, name='logout'),
    path('login', views.loginPage, name='login'),
    path('', views.homepage, name='index'),
    path('perguntas-all', views.topicsPage, name='topics'),
    path('nova-questao', views.newQuestionPage, name='new-question'),
    path('questao/<int:id>', views.questionPage, name='question'),
    path('reply', views.replyPage, name='reply')
]