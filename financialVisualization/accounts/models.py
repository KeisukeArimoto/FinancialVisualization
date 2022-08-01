from ast import List
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


class CustomUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        # create_user と create_superuser の共通処理
        if not email:
            raise ValueError('Email address must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_nomal_user(self, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError('email must be set')

        extra_fields.setdefault('role', 0)

        return self.create_user(email, password, **extra_fields)

    def create_admin_user(self, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError('email must be set')

        extra_fields.setdefault('role', 1)

        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        if not email:
            raise ValueError('email must be set')

        extra_fields.setdefault('is_superuser', 1)
        extra_fields.setdefault('role', 2)

        return self.create_user(email, password, **extra_fields)

    def change_password(self, email, password=None, is_active=True):
        if not email:
            raise ValueError('Email address must be set')

        user = self.get(email=email)
        user.active = is_active
        user.set_password(password)
        user.save(using=self._db)

        return user


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'custom_user'
    # TODO ここにカラムを追加
    username = models.CharField(
        verbose_name='ユーザ名', max_length=255, default='')
    email = models.EmailField(verbose_name='Emailアドレス',
                              max_length=255, unique=True)
    active = models.BooleanField(default=True)
    role = models.IntegerField(verbose_name='ユーザロール', default=0)
    first_name = None
    last_name = None
    is_staff = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_active(self):
        return self.active
