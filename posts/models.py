import uuid
from django.db import models
from django.contrib import messages
from django.core.validators import FileExtensionValidator
from django.core.cache import cache
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from profiles.models import Profile


class PostManager(models.Manager):
    def all_posts(self, profile_list, user_id):
        posts = Post.objects.prefetch_related('author',"comment_posted__user",
            "comment_posted__user__user",'likes').filter(Q(author__in=profile_list) | Q(author__id__exact=user_id))
            
        return posts



class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True)
    content = models.TextField(db_index=True)
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name='profile_liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', db_index=True)
    
    objects = PostManager()

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.likes.all().count()

    # number of comments here
    def num_comments(self):
        return self.comment_posted.all().count()

    
    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_posted')
    body = models.TextField(max_length=500)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body[:20]}---{self.user}"

    


LIKE_CHOICES=(
        ('LIKE', 'like'),
        ('UNLIKE', 'unlike'),
    )
class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=8, choices=LIKE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}---{self.post}---{self.value}"

'''
class Notification(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')    
    
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = (('sender', 'receiver'))

    def __str__(self):
        return f"{self.sender}-{self.receiver}"


# signal to create notification
@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    sender_ = instance.user
    receiver_ = 
    if sender_ != receiver_:
        print('noti reciever')
        
        if instance.status == 'ACCEPTED':
            sender_.friends.add(receiver_.user)
            receiver_.friends.add(sender_.user)
            sender_.save()
            receiver_.save()
        elif instance.status == 'NONE':
            sender_.friends.remove(receiver_.user)
            receiver_.friends.remove(sender_.user)
            instance.delete()
            sender_.save()
            receiver_.save()'''




