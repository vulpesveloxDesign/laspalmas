import os
from django.shortcuts import render, redirect
from django.core.mail import send_mail #, EmailMessage , EmailMultiAlternatives
# from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
# from velox.settings import EMAIL_HOST_USER


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            sender = form.cleaned_data['sender']
            # receiver = os.environ.get('EMAIL_HOST_USER')
            receiver = [os.environ.get('VULPES_EMAIL')]
            send_mail(title, content, sender, receiver, fail_silently=False)

            # email = EmailMessage(title, content, receiver=[to_email])
            # email.send()

            # subject, from_email, to = form.cleaned_data['title'], form.cleaned_data['sender'], os.environ.get('EMAIL_HOST_USER')
            # text_content = form.cleaned_data['content']
            # html_content = '<p>Hey <b>vulpes!</b><br> {1} sent you this a little while ago:</p><p>{0}</p>'.format(form.cleaned_data['content'], form.cleaned_data['sender'])
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            messages.info(request, f'your message has been sent.')
            return redirect('vault:about')
    else:
        form = ContactForm()
    return render(request, 'vault/about.html', {'form':form})

