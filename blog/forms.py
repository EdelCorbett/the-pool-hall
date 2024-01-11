from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-12 col-sm-12'}))
    class Meta:
        model = Comment
        fields = ('body',)