from django.db import models
from django.contrib.auth.models import User

class RegisterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='registermodel')
    userid = models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phoneno = models.BigIntegerField()
    email = models.EmailField(max_length=400, unique=True)
    gender = models.CharField(max_length=200)

    def __str__(self):
        return self.userid

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='No description')
    ingredients = models.TextField()
    steps = models.TextField(default='No steps')
    image = models.ImageField(upload_to='images/', default=None)
    author = models.ForeignKey(RegisterModel, on_delete=models.CASCADE, related_name='recipes')

    def __str__(self):
        return self.name
