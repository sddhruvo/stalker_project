from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Profile
from posts.forms import PostModelForm, CommentModelForm
from posts.models import Post
from relationships.models import Relationship


User = get_user_model()

class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = CommentModelForm
    queryset = Profile.objects.prefetch_related('posts__likes', 'friends', 'posts__comment_posted', 'posts__comment_posted__user')

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        
        
        sender_profile = get_object_or_404(Profile, id=self.request.user.id)
        receiver_profile = get_object_or_404(Profile, id=self.object.id)
        frnd_btn_state = Relationship.objects.relation_status(
            sender=sender_profile,
            receiver=receiver_profile,
        )
        context['frnd_btn_state'] = frnd_btn_state

        context['frnd_req_rcvd'] = Relationship.objects.invitation_recieved(
            receiver = sender_profile
        )
        context['form'] = CommentModelForm()
        return context
    

class ProfilePostComment(SingleObjectMixin, FormView):
    template_name = 'profiles/profile_detail.html'
    form_class = CommentModelForm
    model = Profile

    def post(self, request, *args, **kwargs):
        comment_form = CommentModelForm()
        profile=Profile.objects.get(user=request.user)
        if 'submit_c_form' in request.POST:
            comment_form = CommentModelForm(request.POST or None)
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.user = profile
                post_id = request.POST.get('post_id')
                instance.post = Post.objects.get(id=post_id)
                instance.save()
                comment_form = CommentModelForm()
                return HttpResponseRedirect(self.request.path_info)


    def get_success_url(self):
        return reverse("profiles:detail", kwargs={"slug": self.request.user.username})         

class ProfileDetailComment(View):

    def get(self, request, *args, **kwargs):
        view = ProfileDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProfilePostComment.as_view()
        return view(request, *args, **kwargs)


profile_detail_view = ProfileDetailComment.as_view()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    fields = ["name", 'bio', 'gender', 'country', 
        'favourite',
    ]

    def get_success_url(self):
        return reverse("profiles:detail", kwargs={"slug": self.request.user.username})

    def get_object(self):
        return Profile.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


profile_update_view = ProfileUpdateView.as_view()


class ProfileRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("profiles:detail", kwargs={"slug": self.request.user.username})


profile_redirect_view = ProfileRedirectView.as_view()
