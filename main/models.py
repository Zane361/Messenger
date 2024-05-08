from django.db import models
from django.contrib.auth.models import User
from random import sample
import string


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GroupChat(CodeGenerate):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(upload_to='group-banner/')

    def __str__(self):
        return self.name
    
    @property
    def subscribers_count(self):
        return Subscriber.objects.filter(group=self).count()

    @property
    def admins(self):
        return Admin.objects.filter(group=self)

class Subscriber(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Admin(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    is_super = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Request(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)