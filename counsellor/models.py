from django.db import models
from iCounsel.mixin import TimeStampMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from counsellor.enums import BookingType, Gender, Honorifics, StringBoolChoices, UserType, Religion, Level, MaritalStatus, BookingStatus
from counsellor.managers import CustomUserManager, CustomCounsellorManager
from counsellor.constants import *
from django.utils import timezone

# Create your models here.
class User(TimeStampMixin, AbstractUser):
    # username        = models.CharField(_('Username'), null=False, blank=True, unique=True, max_length=120)
    username        = None
    email           = models.EmailField(_('Email'), null=False, blank=True, unique=True, max_length=120)
    first_name      = models.CharField(_('First Name'), max_length=100)
    last_name       = models.CharField(_('Last Name'), max_length=100)
    other_names     = models.CharField(_('Other Names'), max_length=100, blank=True, null=True)
    is_active       = models.BooleanField(_('Active'), default=False)
    is_staff        = models.BooleanField(_('Admin Access'), default=False)
    is_superuser    = models.BooleanField(_('Superuser'), default=False)
    user_type       = models.CharField(_("User Type"), max_length=25, default=UserType.STUDENT, choices=UserType.choices())
    sex             = models.CharField(_("Sex/Gender"), max_length=20, default=Gender.UNKNOWN, choices=Gender.choices())
    religion        = models.CharField(_("Religion"), max_length=50, default=Religion.OTHER, choices=Religion.choices())
    marital_status  = models.CharField(_("Marital Status"), max_length=50, default=MaritalStatus.SINGLE, choices=MaritalStatus.choices())
    phone           = models.CharField(_('phone'), blank=False, null=False, max_length=10, unique=True)
    address         = models.TextField(_("Address"), blank=True, null=True)
    avatar          = models.ImageField(upload_to="profiles/client/", default=None, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip().title()

    def __str__(self):
        return f"{self.get_full_name()} | {self.email}".upper()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Counsellor(User):
    username        = None
    user_type       = None
    religion        = None
    marital_status  = None
    show_name       = None
    title           = models.CharField(_("Title"), default=Honorifics.MR, choices=Honorifics.choices(), max_length=5)
    profile         = models.ImageField(_('Profile Image'), upload_to="profiles/counselors/", default=None, blank=True, null=True)
    available       = models.BooleanField(_('Available'), default=False)
    fields          = models.ManyToManyField('counsellor.CounsellingType', related_name="counsellors", blank=True)
    description     = models.TextField(_('Short Biography'), max_length=150, null=True,  blank=True)
    availability    = models.ManyToManyField('counsellor.AvailableDay', related_name="counsellor_days_available", blank=False)

    objects = CustomCounsellorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        verbose_name = _('counsellor')
        verbose_name_plural = _('counsellors')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip().title()

    def __str__(self):
        return f"{self.get_full_name()} | {self.email}".upper()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class AvailableDay(TimeStampMixin, models.Model):
    day           = models.CharField(_("Type"), max_length=4, unique=True)

    class Meta:
        verbose_name = _('available day')
        verbose_name_plural = _('available days')
        ordering = ['id']

    def __str__(self):
        return f"{self.day}".upper()

    def save(self, *args, **kwargs):
        if self.day:
            self.day = self.day.upper()
        super(AvailableDay, self).save(*args, **kwargs)


class Booking(TimeStampMixin, models.Model):
    client       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    counsellor   = models.ForeignKey(Counsellor, on_delete=models.CASCADE, related_name="cousellor_bookings")
    meet_id      = models.CharField(_("Meeting ID"), max_length=100, null=True, blank=True)
    booking_type = models.CharField(_("Booking Type"), default=BookingType.VIRTUAL, choices=BookingType.choices(), max_length=20)
    
    start_date   = models.DateField(default=timezone.now, null=False, blank=False)
    start_time   = models.TimeField(default=timezone.now, null=False, blank=False)
    end_time     = models.TimeField(default=timezone.now, null=False, blank=False)

    status       = models.CharField(_("Status"), default=BookingStatus.New, choices=BookingStatus.choices(), max_length=10)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    def __str__(self):
        return f"{self.client.email} - {self.counsellor.email}: {self.status}".upper()


class CounsellingType(TimeStampMixin, models.Model):
    type           = models.CharField(_("Type"), max_length=100, unique=True)

    class Meta:
        verbose_name = _('counselling type')
        verbose_name_plural = _('counselling types')

    def __str__(self):
        return f"{self.type}".upper()


class Consent(TimeStampMixin, models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_consents")

    # Student fields 
    registration_number = models.CharField(_("Registration Number"), default=None, max_length=25, blank=True, null=True, help_text=STUDENT_FIELDS_HELP_TEXT)
    programme           = models.CharField(_("Programme"), default=None, max_length=100, blank=True, null=True, help_text=STUDENT_FIELDS_HELP_TEXT)
    department          = models.CharField(_("Faculty/Department"), default=None, max_length=100, blank=True, null=True, help_text=STUDENT_FIELDS_HELP_TEXT)
    level               = models.CharField(_("Level"), default=None, max_length=10, choices=Level.choices(), blank=True, null=True, help_text=STUDENT_FIELDS_HELP_TEXT)
    residence           = models.CharField(_("Hall of Res./Hostel"), default=None, max_length=100, blank=True, null=True, help_text=STUDENT_FIELDS_HELP_TEXT)
    home_phone          = models.CharField(_("Home Phone"), default=None, max_length=10, blank=True, null=True, help_text=STUDENT_FIELDS_HELP_TEXT)

    # Non-Student fields
    worker              = models.CharField(_("Worker"), max_length=10, default=StringBoolChoices.NO, choices=StringBoolChoices.choices(), blank=True, null=True, help_text=NON_STUDENT_FIELDS_HELP_TEXT)
    work_type           = models.CharField(_("Type Of Work"), max_length=100, blank=True, null=True, help_text=NON_STUDENT_FIELDS_HELP_TEXT)
    organization        = models.CharField(_("Name of Organization"), max_length=100, blank=True, null=True, help_text=NON_STUDENT_FIELDS_HELP_TEXT)

    # General fields
    emergency_person    = models.CharField(_("Emergency Contact Name"), default=None, max_length=100, blank=True, null=True)
    emergency_contact   = models.CharField(_("Emergency Contact Phone"), default=None, max_length=10, blank=True, null=True)
    
    # Other information
    referrer            = models.CharField(_("Referrer"), max_length=100, blank=True, null=True, help_text="Whom may we thank for referring you?")
    prev_counselling    = models.CharField(_("Previous Counselling"), max_length=10, default=StringBoolChoices.NO , choices=StringBoolChoices.choices(), blank=True, null=True, help_text="Any previous counselling on present concern?")
    on_medication       = models.CharField(_("On Prescribed Medication"), max_length=10, default=StringBoolChoices.NO , choices=StringBoolChoices.choices(), blank=True, null=True, help_text="Are you on any pescribed medications?")

    # General fields
    guardian            = models.CharField(_("Guardian Name"), max_length=100, blank=True, null=True, help_text=GUARDIAN_HELP_TEXT)
    guardian_phone      = models.CharField(_("Guardian Phone"), max_length=10, blank=True, null=True, help_text=GUARDIAN_HELP_TEXT)

    def __str__(self):
        return f"{self.user}: {self.counselor}"