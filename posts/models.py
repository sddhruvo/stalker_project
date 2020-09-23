import uuid
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from profiles.models import Profile


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name='profile_liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.likes.all().count()

    # number of comments here
    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
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


# signal to create like counter
@receiver(post_save, sender=Like)
def like_unlike_post(sender, instance, created, **kwargs):
    profile_ = instance.user
    post_ = instance.post
    
    if instance.status == 'LIKE':
        post_.likes.add(profile_.user)
        post_.save()
    elif instance.status == 'UNLIKE':
        post_.likes.remove(profile_.user)
        instance.delete()
        post_.save()




