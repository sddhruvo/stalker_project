from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from profiles.models import Profile
from .models import Relationship

User = get_user_model()


def send_friend_request(request, id):
    sender_profile = get_object_or_404(Profile, id=request.user.id)
    receiver_profile = get_object_or_404(Profile, id=id)
    Relationship.objects.relation_create(
        sender=sender_profile,
        receiver=receiver_profile, status='SEND')
    return redirect('profiles:detail', slug=receiver_profile.slug)

def cancel_sent_friend_request(request, id):
	sender_profile = get_object_or_404(Profile, id=request.user.id)
	receiver_profile = get_object_or_404(Profile, id=id)
	Relationship.objects.relation_delete(
		sender=sender_profile,
		receiver=receiver_profile)

	return redirect('profiles:detail', slug=receiver_profile.slug)


def remove_friend(request, id):
    sender_profile = get_object_or_404(Profile, id=request.user.id)
    receiver_profile = get_object_or_404(Profile, id=id)
    Relationship.objects.relation_delete(
        sender=sender_profile,
        receiver=receiver_profile)

    return redirect('profiles:detail', slug=receiver_profile.slug)



def cancel_friend_request(request, id):
	sender_profile = get_object_or_404(Profile, id=request.user.id)
	receiver_profile = get_object_or_404(Profile, id=id)
	Relationship.objects.relation_delete(
		sender=sender_profile,
		receiver=receiver_profile)

	return redirect('profiles:detail', slug=sender_profile.slug)


def accept_friend_request(request, id):
	sender_profile = get_object_or_404(Profile, id=id)
	receiver_profile = get_object_or_404(Profile, id=request.user.id)
	print(sender_profile, receiver_profile)
	Relationship.objects.relation_accept(
		sender=sender_profile,
		receiver=receiver_profile)

	return redirect('profiles:detail', slug=receiver_profile.slug)


'''
class RelationshipListView(ListView):
	model = Relationship

relationship_list_view = RelationshipListView.as_view()
'''