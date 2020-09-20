from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from .models import Profile
from relationships.models import Relationship


User = get_user_model()

class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    slug_field = "slug"
    slug_url_kwarg = "slug"

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
        return context


profile_detail_view = ProfileDetailView.as_view()

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
