from django.db import models


# Create your models here.

class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    credit = models.IntegerField(default=0)

    def __int__(self):
        return self.uid


class Transaction(models.Model):
    tid = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=30)
    receiver = models.CharField(max_length=30)
    credit = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.tid
