from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .validators import validate_phone_number


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, full_name, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            phone_number=phone_number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,
        unique=True
    )
    phone_number = models.CharField(
        verbose_name="شمارۀ موبایل",
        max_length=11,
        unique=True,
        validators=[validate_phone_number]
    )
    full_name = models.CharField(
        verbose_name="نام و نام خانوادگی",
        max_length=127
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name="ادمین بودن")
    staff_status = models.BooleanField(default=False, verbose_name="داشتن تمام دسترسی ها")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "phone_number"]

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.full_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    receiver = models.CharField(max_length=127, verbose_name='تحویل گیرنده')
    phone = models.CharField(max_length=11, verbose_name='شماره تماس', validators=[validate_phone_number])
    address = models.TextField(verbose_name='نشانی کامل')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    is_active = models.BooleanField(default=True, verbose_name='آدرس فعال')

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
        ordering = ['-is_active']

    def __str__(self):
        return self.postal_code


@receiver(post_save, sender=Address)
def deactivate_other_addresses(sender, instance, **kwargs):
    if instance.is_active:
        Address.objects.exclude(pk=instance.pk, user=instance.user).update(is_active=False)


@receiver(pre_delete, sender=Address)
def activate_last_address(sender, instance, **kwargs):
    if instance.is_active:
        # If the deleted address was active, activate the last one (if exists)
        last_address = Address.objects.filter(user=instance.user).exclude(pk=instance.pk).last()
        if last_address:
            last_address.is_active = True
            last_address.save()
