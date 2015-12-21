#-*- coding:utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    open_id = models.CharField(max_length=100, null=False, blank=False)
    grade = models.IntegerField(default=1, blank=False, null=False)
    user = models.ForeignKey(User,related_name='user_profile')
    def __unicode__(self):
        return self.grade + ':' + self.user.username

class Good(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    grade = models.IntegerField(default=1, blank=False, null=False)
    price = models.DecimalField(max_digits=4, decimal_places=3)
    def __unicode__(self):
        return self.grade + ':' + self.name + ':' + self.price

admin.site.register(UserProfile)
admin.site.register(Good)
