from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin

class User(AbstractUser,PermissionsMixin):
    class Role(models.TextChoices):
        DIRECTOR = "DIRECTOR",'director'


    subject = models.CharField(max_length=150, verbose_name="Subject", null=True, blank=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    role = models.CharField(max_length=15,choices=Role.choices,null=True,blank=True)
    class Meta:
        db_table = "User"
class DirectorManager(BaseUserManager):
    def create_user(self , username , password = None):
        if not username or len(username) <= 0 : 
            raise  ValueError("Username field is required !")
        if not password :
            raise ValueError("Password is must !")
        
        user = self.model(
            username= username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def get_queryset(self,*args,**kwargs):
        result =super().get_queryset(*args,**kwargs)
        return result.filter(role=User.Role.DIRECTOR)
    
class Director(User):
    base_role = User.Role.DIRECTOR
    class Meta:
        proxy = True
    def save(self,*args,**kwargs):
        if not self.pk:
           self.role = self.base_role
           return super().save(*args,**kwargs)
    objects = DirectorManager()
    
