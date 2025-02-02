from django.forms import ModelForm, DateInput, Textarea
from .models import Post, User, Comment


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'is_published',
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'image'
        ]
        widgets = {
            'pub_date': DateInput(attrs={'type': 'date'})
        }


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'rows': 3}),
        }
        labels = {
            'text': 'Ваш комментарий',
        }
