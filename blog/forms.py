## Create "blog/forms.py" to define the CreateArticleForm
# blog/forms.py
# define the forms that we use for create/update/delete operations
 
 
from django import forms
from .models import Article, Comment
 
 
class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database.'''
 
 
    class Meta:
        '''associate this form with a model from our database.'''
        model = Article
        # fields = ['author', 'title', 'text', 'image_url']
        fields = ['author', 'title', 'text', 'image_file']

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
 
 
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        fields = ['author', 'text', ]  # which fields from model should we use

class UpdateArticleForm(forms.ModelForm):
    '''A form to update a quote to the database.'''
 
    class Meta:
        '''associate this form with the Article model.'''
        model = Article
        fields = ['title', 'text', ]  # which fields from model should we use