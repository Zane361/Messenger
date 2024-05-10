from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.UserImages)
admin.site.register(models.Group)
admin.site.register(models.Member)
admin.site.register(models.GroupAdmin)
admin.site.register(models.Request)
admin.site.register(models.Message)
admin.site.register(models.MessageFile)
