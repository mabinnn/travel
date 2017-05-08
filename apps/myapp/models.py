from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re
import bcrypt


class UserManager(models.Manager):

    def register(self, context):
        array = []
        if len(context['first_name']) < 3:
            array.append('First name must be longer than two characters')
        if len(context['last_name']) < 3:
            array.append('Last name must be longer than two characters')
        if not context['first_name'].isalpha():
            array.append('First name must contain alphabets only')
        if not context['last_name'].isalpha():
            array.append('Last name must contain alphabets only')
        if len(context['username']) < 4:
            array.append('Username must be longer than 4 characters')
        if len(context['password']) < 8:
            array.append('Password must be longer than 8 characters!')
        if User.objects.filter(username=context['username']):
            array.append("Username is taken. Please enter a different username.")
        if context['password'] != context['confirm_password']:
            array.append('Passwords are not matching!')
        return array

    def login(self, context):
        array = []
        user_search = User.objects.filter(username=context['username'])
        if not user_search:
            array.append("Username does not exists")
        else:
            registered_user = User.objects.get(username=context['username'])

            if bcrypt.hashpw(context['password'].encode('utf-8'), User.objects.get(username=context['username']).password.encode('utf-8')) != registered_user.password:
                array.append("Incorrect password!")
        return array

class TravelManager(models.Manager):

    def add_travel(self, context):
        array = []
        if len(context['destination']) < 1:
            array.append('Destination cannot be blank!')
        if len(context['end_date']) < 6:
            array.append('Description must be longer than 6 characters')


        return array


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, default='alias')
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Travel(models.Model):
    destination = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    planner = models.ForeignKey(User, related_name='goer')
    joiner = models.ManyToManyField(User, related_name='travelers')
    trip_start = models.DateField()
    trip_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()
