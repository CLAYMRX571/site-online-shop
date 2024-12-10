from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.common.models import BaseModel
import uuid
import datetime
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(("The phone field must be set"))
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.") 
        
        return self.create_user(phone, password, **extra_fields)  

class User(AbstractUser):
    phone = models.CharField(max_length=50, verbose_name="Telefon raqami", unique=True)
    photo = models.ImageField(upload_to='users', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    objects = MyUserManager() 

    def save(self, *args, **kwargs):
        self.username = self.phone 
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
    
EXPIRED_TIME = 5

class PasswordResetCode(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(max_length=255)
    email = models.EmailField()
    expired_time = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=EXPIRED_TIME), editable=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.email}"
