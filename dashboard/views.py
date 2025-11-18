from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post, Category  # Category import karna zaroori hai
from blog.forms import PostForm

@login_required
def dashboard_home(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'dashboard/index.html', {'posts': posts})

@login_required
def create_post(request):
    # Existing categories layenge suggestions ke liye
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save() # Form ka save method ab category khud handle karega
            return redirect('dashboard:home')
    else:
        form = PostForm()
    
    return render(request, 'dashboard/create_post.html', {'form': form, 'categories': categories})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect('dashboard:home')


@login_required
def edit_post(request, pk):
    # Sirf wahi post edit hogi jo logged-in user ki hai
    post = get_object_or_404(Post, pk=pk, author=request.user)
    categories = Category.objects.all() # Suggestions ke liye
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard:home')
    else:
        form = PostForm(instance=post)
        # Logic: Agar purani category hai, toh use Text Box mein pre-fill kar do
        if post.category:
            form.fields['category_input'].initial = post.category.name

    return render(request, 'dashboard/edit_post.html', {
        'form': form, 
        'categories': categories
    })