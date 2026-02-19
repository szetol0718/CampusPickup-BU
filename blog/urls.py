# blog/urls.py

from django.urls import path
from .views import ShowAllView, ArticleView # our view class definition 
from .views import RandomArticleView, CreateArticleView, CreateCommentView
 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # show one article
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
]
 