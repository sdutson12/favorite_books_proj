from django.db import models
import re

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_conf']:
            errors["password"] = "Passwords don't match"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) == 0:
            errors["password"] = "Password cannot be empty"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        try:
            User.objects.get(email=postData['email'])
        except:
            errors["email"] = "No user with that email address"
        return errors
    def new_book_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors["title"] = "Title cannot be empty"
        if len(postData['desc']) < 5:
            errors["desc"] = "Description should be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=70)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()