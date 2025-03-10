from django.db import models

# Create your models here.
class User(models.Model): # класс представляющий пользователя
    username = models.CharField(max_length=200, unique=True) # имя пользователя
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username