from django.shortcuts import render
from blog.models import Post
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    recent_posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/index.html', {'recent_posts': recent_posts})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Data nikalo
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Email Format
            full_message = f"Message from {name} ({email}):\n\n{message}"

            try:
                # Email Bhejo (Sender: User ka email, Receiver: Aapka email)
                send_mail(
                    f"Contact Form: {subject}", # Email Subject
                    full_message,               # Email Body
                    settings.EMAIL_HOST_USER,   # From Email
                    [settings.EMAIL_HOST_USER], # To Email (Aap hi ko milega)
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent! We'll get back to you soon.")
                return redirect('core:contact')
            except Exception as e:
                messages.error(request, "Something went wrong. Please try again later.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})