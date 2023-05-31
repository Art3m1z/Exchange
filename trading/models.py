import uuid

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен ввести электронную почту!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name="адресом электронной почты")
    phone = models.CharField(null=False, blank=False, unique=True, max_length=12, verbose_name='Номер телефона',
                             validators=[RegexValidator("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")]
                             )
    first_name = models.CharField(max_length=32, verbose_name='Имя')
    last_name = models.CharField(max_length=32, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=32, verbose_name='Отчество', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", 'last_name', "middle_name", 'phone', "is_staff"]

    def get_full_name(self):
        if self.middle_name is not None:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        else:
            return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return f"{self.email} {self.get_full_name()}"

    class Meta:
        ordering = '-id'
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'


class Assets(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Order(models.Model):
    MAIN_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('EXECUTED', 'Executed'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    main = models.CharField(choices=MAIN_CHOICES, max_length=4)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)


class MarketData(models.Model):
    asset = models.OneToOneField(Assets, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.asset} {self.price}"


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.asset} {self.user}"