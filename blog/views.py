from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm
from django.db.models import Q
from django.core.paginator import Paginator

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})



def search(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        # Title YA Body mein dhoondo (Case insensitive)
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).order_by('-created_at')
    
    return render(request, 'blog/search.html', {'query': query, 'results': results})


def post_list(request):
    # Saare posts nikalo
    posts_list = Post.objects.all().order_by('-created_at')
    
    # Pagination Logic: Har page par sirf 6 posts dikhao
    paginator = Paginator(posts_list, 6) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_list(request):
    # 1. URL se category maango (e.g., ?category=Gaming)
    category_filter = request.GET.get('category')
    
    # 2. Saare posts lo
    posts_list = Post.objects.all().order_by('-created_at')
    
    # 3. Agar filter aaya hai, toh posts ko chatni (filter) karo
    if category_filter:
        posts_list = posts_list.filter(category__name=category_filter)

    # 4. Saari Categories bhi bhejo taaki buttons ban sakein
    categories = Category.objects.all()

    # 5. Pagination (Same as before)
    paginator = Paginator(posts_list, 6) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'categories': categories,
        'current_category': category_filter # Ye active button highlight karne ke liye
    }
    return render(request, 'blog/post_list.html', context)