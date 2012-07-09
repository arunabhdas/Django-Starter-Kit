from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='user_profile')

    address = models.TextField(_('address'))
    city = models.CharField(_('city'), max_length=255)
    state = USStateField(_('state'))
    zipcode = models.CharField(_('zipcode'), max_length=255)


# Signal Handlers
# -----------------
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        new_profile, new = UserProfile.objects.get_or_create(user=instance)
