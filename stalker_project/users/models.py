import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for stalker_project."""

    #: First and last name do not cover name patterns around the globe
    first_name = CharField(max_length=128, null=True, blank=False)
    last_name = CharField(max_length=128, null=True)
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("profiles:detail", kwargs={"slug": self.username})
    
