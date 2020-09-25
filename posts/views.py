from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Like, Comment
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm



@login_required
def post_comment_create_and_list_view(request):
    profile = Profile.objects.select_related('user').get(user=request.user).get_all_friends_list()
    #profile contains list of the friends i have
    queryset = Post.objects.all_posts().filter(Q(author__in=profile) | Q(author__id__exact=request.user.id))
    

    #post form
    post_form = PostModelForm()
    if 'submit_p_form' in request.POST:
        post_form = PostModelForm(request.POST or None, request.FILES or None)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            messages.success(request, 'Post published')
            return redirect('posts:main_post_list')
    
    #comment form
    comment_form = CommentModelForm()
    if 'submit_c_form' in request.POST:
        comment_form = CommentModelForm(request.POST or None)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            post_id = request.POST.get('post_id')
            instance.post = Post.objects.get(id=post_id)
            instance.save()
            comment_form = CommentModelForm()
            return redirect('posts:main_post_list')

    context = {
        'queryset': queryset,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
    }
    return render(request, 'posts/main.html', context)

        

def like_unlike_post(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        print(post_obj)
        profile = Profile.objects.get(user=user)
        print(profile)

        if profile in post_obj.likes.all():
            print(1)
            post_obj.likes.remove(profile)
        else:
            print(2)
            post_obj.likes.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            print(3)
            if like.value=='LIKE':
                print(4)
                like.value='UNLIKE'
            else:
                print(5)
                like.value='LIKE'
        else:
            print(6)
            like.value='LIKE'

            post_obj.save()
            like.save()

    return redirect('posts:main_post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main_post_list')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = Post.objects.get(id=id)

        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You can\'t delete others post!')
            return redirect('posts:main_post_list')
        return obj

class PostUpdateView(UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main_post_list')

    def form_valid(self, form):
        profile = Profile.objects.get(user = self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Hey!! You are not the owner of this post!')
            return super().form_invalid(form)


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main_post_list')

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = Comment.objects.get(id=id)

        if not obj.user.user == self.request.user:
            messages.warning(self.request, 'Hey!! You are not the owner of this post!')
            return redirect('posts:main_post_list')
        return obj

class CommentUpdateView(UpdateView):
    form_class = CommentModelForm
    model = Comment
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main_post_list')

    def form_valid(self, form):
        profile = Profile.objects.get(user = self.request.user)
        if form.instance.user.id == profile.id:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Hey!! You are not the owner of this post!')
            return super().form_invalid(form)