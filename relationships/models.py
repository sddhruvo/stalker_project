from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from profiles.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


RELATION_STATUS_CHOICES = (
    ('NONE', 'none'),
    ('SEND', 'send'),
    ('ACCEPTED', 'accepted')
)

class RelationshipManager(models.Manager):
    def invitation_recieved(self, receiver):
        queryset = Relationship.objects.filter(receiver=receiver, status='SEND')
        return queryset
    
    def relation_create(self, sender, receiver, status='SEND'):
        relation = Relationship.objects.create(sender=sender, receiver=receiver, status=status)
        relation.save()
        return relation

    def relation_accept(self, sender, receiver):
        relation = Relationship.objects.get(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        )
        relation.status = 'ACCEPTED'
        relation.save()
    
    def relation_delete(self, sender, receiver):
        relation = Relationship.objects.get(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        )
        relation.status = 'NONE'
        relation.save()

    def relation_status(self, sender, receiver):
        try:
            relation = Relationship.objects.get(
                Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
            )
            status = relation.status
        except ObjectDoesNotExist:
            status = 'NONE' 
        return status


    

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')    
    status = models.CharField(max_length=8, choices = RELATION_STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    class Meta:
        unique_together = (('sender', 'receiver'))

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


# signal to create relation
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if sender_ != receiver_:
        if instance.status == 'ACCEPTED':
            print('postsaveaccept')
            sender_.friends.add(receiver_.user)
            receiver_.friends.add(sender_.user)
            sender_.save()
            receiver_.save()
        elif instance.status == 'NONE':
            print('postsavedelete')
            sender_.friends.remove(receiver_.user)
            receiver_.friends.remove(sender_.user)
            instance.delete()
            sender_.save()
            receiver_.save()


