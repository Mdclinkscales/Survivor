from django.db import models
import re
import bcrypt
# Create your models here.

class manager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if len(postData['firstname'])< 2:
            errors['firstname'] = 'no single character first names'
        if len(postData['lastname'])< 2:
            errors['lastname'] = 'no single character last names'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address'
        if len(postData['password']) < 8:
            errors['password'] = 'Need password of at least 8 characters'
        if postData['password'] != postData['confirmpassword']:
            errors['confirmpassword'] = 'The passwords must match'
        if len(User.objects.filter(email = postData['email'])) is not 0:
            errors['email'] = 'Email already registered for a different user'
        return errors
    
    def loginvalidator(self, postData):
        errors = {}
        user = User.objects.get(email=postData['useremail'])
        if bcrypt.checkpw(postData['userpass'].encode(), user.password.encode()):
            print('pass matches')
        else:
            errors['loginpass'] = 'that aint the password m8'
        return errors

class User(models.Model):
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 30)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = manager()