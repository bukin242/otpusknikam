# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class SiteUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError(u'У пользователя должен быть e-mail адрес')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):

        user = self.create_user(email, password=password, **kwargs)
        user.is_admin = True
        user.save(using=self._db)

        return user


class SiteUser(AbstractBaseUser):

    email = models.EmailField(verbose_name=u'e-mail адрес', max_length=255, unique=True)
    create_date = models.DateTimeField(null=True, db_index=True, blank=True, auto_now_add=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)

    objects = SiteUserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class ProfilePublishedManager(models.Manager):

    def get_queryset(self):
        return super(ProfilePublishedManager, self).get_queryset() \
            .filter(is_active=True)


class Profile(SiteUser):

    user = models.OneToOneField(SiteUser, verbose_name=_('user'), related_name='%(class)s', primary_key=False)
    balance = models.IntegerField(u'баланс', default=settings.BONUS)

    name = models.CharField(u'имя на сайте', max_length=255)
    subscribe = models.BooleanField(u'подписка на предложения', db_index=True, default=False)

    objects = SiteUserManager()
    published = ProfilePublishedManager()

    class Meta:
        verbose_name = u'профиль'
        verbose_name_plural = u'профили'
