from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.views.generic import (
    DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy, reverse

from .forms import PostCreateForm, ProfileForm, CommentForm
from .models import Category, Post, User, Comment
from .mixins import OnlyAuthorMixin, CommentMixin
from .utils import get_filtered_qs, send_test_email

PAGINATE_COUNT = 10


class IndexView(ListView):
    """CBV-index"""

    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = PAGINATE_COUNT

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = get_filtered_qs(queryset)
        return queryset.select_related('author').prefetch_related(
            'category',
            'location'
        )


class PostView(DetailView):
    """CBV-post"""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            user_posts = Q(author=self.request.user)
            published_posts = Q(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            )
            return (
                queryset
                .filter(user_posts | published_posts)
                .select_related('author')
                .prefetch_related('category', 'location', 'comments')
            )
        return (
            get_filtered_qs(queryset)
            .select_related('author')
            .prefetch_related('category', 'location', 'comments')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('created_at')
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.object.author.username
        return reverse('blog:profile', args=[username])


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        if not self.test_func():
            return redirect(reverse(
                'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
            ))

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryView(DetailView):
    """CBV-category"""

    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category'
    paginate_by = PAGINATE_COUNT

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = get_filtered_qs(
            Post.objects,
            category=self.object
        ).select_related('author', 'location').order_by('-pub_date')
        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProfileView(TemplateView):
    """CBV-profile"""

    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_COUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        profile = get_object_or_404(User, username=username)
        if profile == self.request.user:
            posts = (
                Post.objects.filter(author=profile)
                .order_by('-pub_date')
                .annotate(comment_count=Count('comments'))
            )
        else:
            posts = (
                get_filtered_qs(Post.objects, author=profile)
                .order_by('-pub_date')
            )

        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['profile'] = profile
        context['page_obj'] = page_obj
        return context


class ProfileEditView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        post_id = self.kwargs.get('post_id')
        return reverse('blog:post_detail', kwargs={'post_id': post_id})

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditCommentView(CommentMixin, UpdateView):
    form_class = CommentForm
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context
