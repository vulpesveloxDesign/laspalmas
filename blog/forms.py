from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'content',
            'slug'
        ]

    def clean_title(self):
        banned_titles = ['create', 'admin', 'vulpes']
        title = self.cleaned_data.get('title')
        if title in banned_titles:
            raise forms.ValidationError('you\'re gonna have to try harder!')
        return title

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if '.edu' in email:
    #         raise forms.ValidationError('we don\'t want your stinking .edu emails!')
    #     return email

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
