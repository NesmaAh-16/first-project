from django.db import models
import re
from datetime import datetime , date
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 4:
            errors['first_name'] = "First name must be at least 4 characters."
        if len(postData['last_name']) < 4:
            errors['last_name'] = "Last name must be at least 4 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email is already registered."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_pw']:
            errors['confirm'] = "Passwords do not match."
        if not postData['date_of_birth']:
            errors['date_of_birth'] = "date_of_birth is required."
        else:
            bday = datetime.strptime(postData['date_of_birth'], '%Y-%m-%d').date()
            if bday >= date.today():
                errors['date_of_birth'] = "date_of_birth must be in the past."
            else:
                age = (date.today() - bday).days // 365
                if age < 18:
                    errors['date_of_birth'] = "You must be at least 18 years old to register."
        return errors

class GameManager(models.Manager):
    def game_validator(self, postData):
        errors = {}
        name = postData.get('name', '').strip()
        if not name:
            errors['name']="Game name is required."
        else:   
            if len(postData['name']) < 2:
                errors['name'] = "Game name must be at least 2 characters."
                
        if not postData['genre']:
            errors['genre']="Game genre is required."        
    
        if not postData['release_date']:
            errors["release_date"] = "Release date is required."
        else:
            release_date = datetime.strptime(postData['release_date'], '%Y-%m-%d')
            if release_date > datetime.now():
                errors["release_date"] = "Release date must not be in the future."
                
        desc= postData.get('desc', '').strip()
        if not desc:
            errors['desc']="Game description is required." 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    password = models.CharField(max_length=255)
    upload_avatar=models.ImageField(upload_to='product_images/', null=True) #python -m pip install Pillow
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Game(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    desc = models.TextField(blank=False) # Cannot be blank in forms  
    created_by = models.ForeignKey(User, related_name="games_created", on_delete=models.CASCADE ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GameManager()