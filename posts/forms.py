from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    content = forms.CharField(label='',
        widget=forms.Textarea(attrs={
            'rows': 4, 'placeholder': 'Tell the world!',
            'class': 'bg-gray-100'
    }))
    class Meta:
        model = Post
        fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
            widget=forms.Textarea(attrs={'rows': 2,'placeholder': 'Add a commnet'}))
    class Meta:
        model = Comment
        fields = ('body',)