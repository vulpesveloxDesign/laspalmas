from django import forms

class ContactForm(forms.Form):
    title           = forms.CharField(label='title', max_length=120, required=True)
    content         = forms.CharField(label='content', widget=forms.Textarea, required=True)
    sender          = forms.EmailField(label='sender', required=True)
