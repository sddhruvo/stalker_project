import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    GENDER = [
        ('NONE', 'none'),
        ('MALE', 'male'),
        ('FEMALE', 'female')
    ]
    name = models.CharField(max_length=200, blank=True)
    id = models.UUIDField(primary_key=True, editable=False)
    bio = models.TextField(default='No bio data', max_length=400)
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=6, choices=GENDER, default='NONE')
    country = CountryField()
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name='friends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    favourite = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(unique=True,blank=True)
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        self.id = self.user.id
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_all_friends(self):
        return self.friends.all()

    def get_absolute_url(self):
        """Get url for profile's detail view.

        Returns:
            str: URL for profile detail.

        """
        return reverse("profiles:detail", kwargs={"slug": self.slug})


# signal to create profile for user created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()