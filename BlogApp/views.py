from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm, PostCreateForm, PostSearchForm, PostUpdateForm
from .models import Post, User, Bookmark


class PostListView(ListView):
    template_name = "post-list.html"
    model = Post
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if self.request.user.is_authenticated:
            bookmark_id_list = Bookmark.objects.filter(user=user).values_list('post_id', flat=True)
            context['bookmark_post_id_list'] = bookmark_id_list

        return context

    def get_queryset(self):
        post_list = Post.objects.order_by('-creation_date')
        return post_list

class PostMyListView(LoginRequiredMixin, ListView):
    template_name = "post-my-list.html"
    model = Post
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        bookmark_id_list = Bookmark.objects.filter(user=user).values_list('post_id', flat=True)
        context['bookmark_post_id_list'] = bookmark_id_list

        return context

    def get_queryset(self):
        post_list = Post.objects.filter(author=self.request.user).order_by('-creation_date')
        return post_list


class PostBookmarkListView(LoginRequiredMixin, ListView):
    template_name = "post-bookmark-list.html"
    model = Post
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        bookmark_id_list = Bookmark.objects.filter(user=user).values_list('post_id', flat=True)
        context['bookmark_post_id_list'] = bookmark_id_list

        return context

    def get_queryset(self):
        user = self.request.user
        post_list = Post.objects.filter(bookmarks__user=user)
        return post_list


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post-create.html'
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        messages.success(self.request, 'Create post')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'post-update.html'
    model = Post
    form_class = PostUpdateForm
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        post = form.save(commit=False)
        messages.success(self.request, 'Update post')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post-list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Successfully deleted')
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

class PostSearchView(ListView):
    paginate_by = 5
    template_name = 'post-search.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title = self.request.GET.get('title')
        content = self.request.GET.get('content')
        author_id = self.request.GET.get('author_id')
        creation_date = self.request.GET.get('creation_date')

        initial_value = {
            'title': title,
            'content': content,
            'author_id': author_id,
            'creation_date': creation_date
        }

        context['post_search_form'] = PostSearchForm(initial=initial_value)

        additional_query = f'&search=true&title={title if title else ""}&content={content if content else ""}&author_id={author_id if author_id else ""}&creation_date={creation_date if creation_date else ""}'

        context['additional_query'] = additional_query

        user = self.request.user
        if self.request.user.is_authenticated:
            bookmark_id_list = Bookmark.objects.filter(user=user).values_list('post_id', flat=True)
            context['bookmark_post_id_list'] = bookmark_id_list

        return context

    def get_queryset(self):

        title = self.request.GET.get('title')
        content = self.request.GET.get('content')
        author_id = self.request.GET.get('author_id')
        creation_date = self.request.GET.get('creation_date')

        search = self.request.GET.get('search')

        if search:
            post_list = Post.objects.all()

            if title:
                post_list = post_list.filter(title__contains=title)
            if content:
                post_list = post_list.filter(content__contains=content)
            if author_id:
                post_list = post_list.filter(author__pk=author_id)
            if creation_date:
                post_list = post_list.filter(creation_date=creation_date)
            return post_list.order_by('-creation_date')

        else:
            return Post.objects.none()

class UserListView(ListView):
    template_name = "user-list.html"
    model = User
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_post_count_dict = dict()

        user_list = User.objects.all().filter(is_superuser=False)

        for user in user_list:
            user_post_count_dict[user.id] = user.posts.count()

        context['user_post_count_dict'] = user_post_count_dict

        return context

    def get_queryset(self):
        user_list = User.objects.all().filter(is_superuser=False).order_by('username')
        return user_list

class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)

        messages.success(self.request, 'Successfully sign up')

        return response

class BlogLoginView(LoginView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, "Successfully log in")
        return super().form_valid(form)

class BlogLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "post-list.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Successfully log out')
        return response


@login_required
def create_bookmark(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    Bookmark.objects.create(user=user, post=post)

    return JsonResponse({'status': 'success'})


@login_required
def delete_bookmark(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    Bookmark.objects.filter(user=user, post=post).delete()

    return JsonResponse({'status': 'success'})
