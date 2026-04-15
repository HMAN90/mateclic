from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class User(models.Model):
    class Roles(models.TextChoices):
        PR = "provider"
        CS = "customer"
    firstName = models.fields.CharField(max_length=100,null=True)
    lastName = models.fields.CharField(max_length=100,null=True)
    companyName = models.fields.CharField(max_length=100,null=True)
    summary = models.fields.CharField(max_length=100,null=True)
    logo = models.FileField(upload_to='providers/',null=True)
    email = models.fields.CharField(max_length=100,unique=True)
    password = models.fields.CharField(max_length=1000)
    countryCode = models.fields.IntegerField(default=243)
    phone = models.fields.CharField(max_length=20,null=True)
    confirmationCode = models.fields.IntegerField(null=True)
    confirmed = models.fields.BooleanField(default=False)
    role = models.fields.CharField(choices=Roles.choices)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        Fournisseur = "provider"
        Client = "customer"
    email = models.EmailField(unique=True)
    #username = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.fields.CharField(choices=Roles.choices,null=True)
    

    companyName = models.fields.CharField(max_length=100,null=True)
    summary = models.fields.CharField(max_length=100,null=True)
    logo = models.FileField(upload_to='providers/',null=True)
    email = models.fields.CharField(max_length=100,unique=True)
    password = models.fields.CharField(max_length=1000)
    countryCode = models.fields.IntegerField(default=243)
    phone = models.fields.CharField(max_length=20,null=True)
    confirmationCode = models.fields.IntegerField(null=True)
    confirmed = models.fields.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    confirmedAt = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # No username required if email is the USERNAME_FIELD

    def __str__(self):
        return self.email
class Category(models.Model):
    name= models.fields.CharField(unique=True)
    parent = models.ForeignKey('self',null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
class Equipment(models.Model):
    class Frequencies(models.TextChoices):
        H = "hour"
        D = "day"
        M = "month"
    class Currencies(models.TextChoices):
        USD = "Dollar"
        CDF = "Franc Congolais"
  
    name = models.fields.CharField(max_length=None)
    description = models.fields.CharField(max_length=None,null=True)
    location = models.fields.CharField(max_length=None,null=True)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    owner = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    pricingFrequency = models.fields.CharField(choices=Frequencies.choices)
    price = models.fields.DecimalField(null=True,max_digits=100,decimal_places=2)
    currency = models.fields.CharField(choices=Currencies.choices)
    image = models.FileField(upload_to='equipments/',null=True)
    createdAt = models.DateTimeField(auto_now=True)

class Rent(models.Model):
    duration = models.fields.DecimalField(null=True, max_digits=100,decimal_places=1)
    equipment = models.ForeignKey(Equipment,null=True,on_delete=models.SET_NULL)
    quantity = models.fields.IntegerField(default=1)
    customer = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    state = models.fields.CharField(null=True,default="created")
    paymentMethod = models.fields.CharField(default="mobileMoney")
    numberPhone = models.fields.CharField(null=True)
    mobileMoneyPhone = models.fields.CharField(null=True)
    paymentToken = models.fields.CharField(null=True)
    paymentId = models.fields.CharField(null=True)
    rentStart= models.fields.DateTimeField(null=True)
    rentEnd= models.fields.DateTimeField(null=True)
    createdAt= models.fields.DateTimeField(auto_now=True)
    receiptCode = models.fields.CharField(null=True)
    rentTotalAmount = models.fields.DecimalField(null=True,max_digits=100,decimal_places=2)
    currency = models.fields.CharField(null=True,default="usd")
class Withdraw(models.Model):

    provider = models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    state = models.fields.CharField(null=True,default="created")
    withdrawMethod = models.fields.CharField(default="mobileMoney")
    mobileMoneyPhone = models.fields.CharField(null=True)
    
    createdAt= models.fields.DateTimeField(auto_now=True)
    confirmedAt= models.fields.DateTimeField(null=True)
    transactionCode = models.fields.CharField(null=True)
    amount = models.fields.DecimalField(null=True,max_digits=100,decimal_places=2)
    currency = models.fields.CharField(null=True,default="usd")