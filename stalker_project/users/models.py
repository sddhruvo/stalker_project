import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, UUIDField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for stalker_project."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("profiles:detail", kwargs={"slug": self.username})
    
