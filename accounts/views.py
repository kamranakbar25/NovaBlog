from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import Follow
from blog.models import Post

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from .models import Follow, UserProfile

from django.contrib.auth import logout

import random
from django.core.mail import send_mail
from django.conf import settings




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 1. User ka data session (temporary memory) mein save kar lo
            # Database mein abhi save nahi karenge
            request.session['user_data'] = form.cleaned_data
            
            # 2. OTP Generate karo (4 digit)
            otp = str(random.randint(1000, 9999))
            request.session['otp'] = otp  # OTP ko bhi session mein rakho match karne ke liye
            
            # 3. Email Bhejo
            email = form.cleaned_data.get('email')
            subject = 'Verify your Email - NovaBlog'
            message = f'Hello! Your OTP for NovaBlog registration is: {otp}'
            
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                messages.success(request, f'OTP sent to {email}')
                return redirect('accounts:verify_otp')  # OTP page par bhejo
            except Exception as e:
                messages.error(request, "Error sending email. Please try again.")
                return redirect('accounts:register')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('otp')
        user_data = request.session.get('user_data')

        if not user_data:
            messages.error(request, "Session expired. Please register again.")
            return redirect('accounts:register')

        if entered_otp == generated_otp:
            # --- SUCCESS: OTP Match ho gaya ---
            
            # Yahan hum check kar rahe hain ki password kis key mein hai
            # 'password' ya 'password1' (jo bhi available ho)
            final_password = user_data.get('password') or user_data.get('password1')

            # 1. User Create karo
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=final_password  # Corrected password variable
            )
            user.save()
            
            # 2. Profile Create karo
            UserProfile.objects.create(user=user)

            # 3. Session clear karo
            if 'otp' in request.session: del request.session['otp']
            if 'user_data' in request.session: del request.session['user_data']

            # 4. Login Page par bhejo
            messages.success(request, "Account verified successfully! You can now login.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'accounts/otp_verify.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def public_profile(request, username):
    # Jis author ki profile khol rahe hain, use dhoondo
    author = get_object_or_404(User, username=username)
    
    # Us author ke saare posts nikalo
    posts = Post.objects.filter(author=author).order_by('-created_at')
    
    # Check karo ki kya logged-in user isse already follow kar raha hai?
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=author).exists()
    
    # Followers count
    followers_count = author.followers.count()
    following_count = author.following.count()

    context = {
        'author': author,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    }
    return render(request, 'accounts/public_profile.html', context)

@login_required
def follow_toggle(request, username):
    author = get_object_or_404(User, username=username)
    
    # Khud ko follow nahi kar sakte
    if request.user == author:
        messages.warning(request, "You can't follow yourself!")
        return redirect('accounts:public_profile', username=username)

    # Check karo pehle se follow hai ya nahi
    follow_record = Follow.objects.filter(follower=request.user, following=author)
    
    if follow_record.exists():
        follow_record.delete() # Agar hai to Unfollow kar do
        messages.info(request, f"Unfollowed {username}")
    else:
        Follow.objects.create(follower=request.user, following=author) # Nahi hai to Follow kar do
        messages.success(request, f"You are now following {username}")
        
    return redirect('accounts:public_profile', username=username)


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Yahan hum 'profile' variable use kar rahe hain jo humne upar get_or_create se liya
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('core:home')