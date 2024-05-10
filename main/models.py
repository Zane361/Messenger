from django.db import models
from django.contrib.auth.models import AbstractUser
from random import sample
import string
import os

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


class User(AbstractUser):
    phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

    @property
    def groups(self):
        return Group.objects.filter(user=self)
    
    @property
    def avatar(self):
        return UserImages.objects.filter(user=self).last()
    

class UserImages(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user-image/')
    date = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        super(UserImages, self).delete(*args, **kwargs)

    
class Group(CodeGenerate):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(upload_to='group-banner/')

    def __str__(self):
        return self.name
    
    @property
    def members_count(self):
        return Member.objects.filter(group=self).count()

    @property
    def admins(self):
        return GroupAdmin.objects.filter(group=self)
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            super(Group, self).save(*args, **kwargs)  
            GroupAdmin.objects.get_or_create(user=self.user, group=self, is_super=True)
            Member.objects.get_or_create(user=self.user, group=self, is_admin=True)
        else:
            super(Group, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.banner:
            banner_path = self.banner.path
            if os.path.exists(banner_path):
                os.remove(banner_path)
        super(Group, self).delete(*args, **kwargs)


class Member(CodeGenerate):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not Member.objects.filter(user=self.user, group=self.group).exists():
            if self.is_admin:
                GroupAdmin.objects.get_or_create(user=self.user, group=self.group, is_super=False)
                super(Member, self).save(*args, **kwargs)
            else:
                super(Member, self).save(*args, **kwargs)
        else:
            if Member.objects.filter(user=self.user, group=self.group)[0].pk == self.pk:
                if self.is_admin:
                    GroupAdmin.objects.get_or_create(user=self.user, group=self.group, is_super=False)
                    super(Member, self).save(*args, **kwargs)
                else:
                    super(Member, self).save(*args, **kwargs)
            else:
                raise ValueError('Bu foydalanuvchi guruhda allaqachon mavjud!')


class GroupAdmin(CodeGenerate):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_super = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not GroupAdmin.objects.filter(user=self.user, group=self.group).exists() or not self.pk:
            super(GroupAdmin, self).save(*args, **kwargs)
        else:
            if GroupAdmin.objects.filter(user=self.user, group=self.group)[0].pk == self.pk:
                super(GroupAdmin, self).save(*args, **kwargs)
            else:
                raise ValueError('Bu foydalanuvchida adminlik allaqachon mavjud!')

class Request(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.user.pk:
            self.user.save()
        if not self.group.pk:
            self.group.save()

        something = Request.objects.filter(user=self.user, group=self.group)
        if something.count() == 0 or ((something.count() == 1 and not something[0].is_rejected) and self.is_rejected):
            if Member.objects.filter(user=self.user, group=self.group).count() == 0:
                super(Request, self).save(*args, **kwargs)
            else:
                raise ValueError("Bu foydalanuvchi guruhda allaqachon mavjud!")
        else:
            raise ValueError("Bu foydalanuvchining so'rovi allaqachon mavjud!")

    def delete(self, *args, **kwargs):
        Member.objects.create(
            user = self.user,
            group = self.group,
            is_admin = False,
        )
        super(Request, self).delete(*args, **kwargs)


class Message(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if Member.objects.filter(user=self.user, group=self.group).count() == 1:
            super(Message, self).save(*args, **kwargs)
        else:
            raise ValueError("Bu foydalanuvchi guruh a'zosi emas!")


class MessageFile(CodeGenerate):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to='message-file/')

    def __str__(self):
        return self.message.text

    def delete(self, *args, **kwargs):
        if self.file:
            file_path = self.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super(MessageFile, self).delete(*args, **kwargs)