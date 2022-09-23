from django.db import models
from iCounsel.mixin import TimeStampMixin
from shortuuid.django_fields import ShortUUIDField

# Create your models here.
class Session(TimeStampMixin, models.Model):
    session_id          = ShortUUIDField(length=4, max_length=9, alphabet="0123456789abcdefghijABCDEFGHIJ", primary_key=True, editable=False, null=False)
    user                = models.ForeignKey("counsellor.User", on_delete=models.CASCADE, related_name="user_sessions")
    counselor           = models.ForeignKey("counsellor.Cousellor", on_delete=models.SET_NULL, related_name="cousellor_sessions", null=True, blank=True)
    active              = models.BooleanField(default=False)

    indexes = [models.Index(fields=['session_id']), ]
