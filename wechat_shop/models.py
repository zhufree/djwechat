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
    discount = models.DecimalField(default=0.85, max_digits=2, decimal_places=2)
    raw_price = models.DecimalField(default=0.00, max_digits=4, decimal_places=3)
    final_price = models.DecimalField(default=0.00, max_digits=4, decimal_places=3)

    def compute(self):
        pass

    def __unicode__(self):
        return self.grade + ':' + self.name + ':' + self.raw_price

admin.site.register(UserProfile)
admin.site.register(Good)
