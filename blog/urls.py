# blog/urls.py

from django.urls import path
from .views import ArticleListAPIView, ShowAllView, ArticleView # our view class definition 
from .views import RandomArticleView, CreateArticleView, CreateCommentView
from .views import UpdateArticleView, DeleteCommentView, RegistrationView
from django.contrib.auth import views as auth_views    ## NEW
from .views import *
 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # show one article
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"), 
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
    # authentication views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
    path('register/', RegistrationView.as_view(), name='register'),
    # API views:   
    path(r'api/articles/', ArticleListAPIView.as_view(),name = 'api_show_all'),
    path(r'api/article/<int:pk>', ArticleDetailAPIView.as_view()),
]
 