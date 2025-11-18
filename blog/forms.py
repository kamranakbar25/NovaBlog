from django import forms
from .models import Post, Comment, Category

# --- POST FORM (With Rich Text Editor & Smart Category) ---
class PostForm(forms.ModelForm):
    category_input = forms.CharField(
        label="Category",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 rounded bg-gray-50 border focus:ring-2 focus:ring-indigo-500 outline-none',
            'placeholder': 'Type a category (e.g., Gaming, Coding)...',
            'list': 'category-list'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded bg-gray-50 border focus:ring-2 focus:ring-indigo-500 outline-none'
            }),
            
            # 👇 YEH HAI WO CLASS JO EDITOR KO ACTIVATE KAREGI
            'body': forms.Textarea(attrs={
                'class': 'rich-editor w-full p-3 rounded bg-gray-50 border focus:ring-2 focus:ring-indigo-500 outline-none', 
                'rows': 20
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        cat_name = self.cleaned_data['category_input']
        category_obj, created = Category.objects.get_or_create(name=cat_name.title())
        instance.category = category_obj
        
        if commit:
            instance.save()
        return instance


# --- COMMENT FORM (Ye missing tha, isliye error aaya) ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl bg-gray-50 focus:ring-2 focus:ring-indigo-500 outline-none', 'placeholder': 'Your Name'}),
            'body': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl bg-gray-50 focus:ring-2 focus:ring-indigo-500 outline-none', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }