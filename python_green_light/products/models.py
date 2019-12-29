from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField()
    url = models.TextField()
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    votes_total = models.IntegerField(default=0)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=5)
    liked_projects = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Категория')

    def __str__(self):
        return self.name



