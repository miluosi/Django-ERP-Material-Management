from curses.ascii import isdigit
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class EUser(User):
    def validate_phone(string):
        if len(string) != 11:
            raise ValidationError("Enter a valid 11-digit phone number.")
        if string[0] != '1':
            raise ValidationError("Enter a valid phone number beginning with '1'.")
        for s in string:
            if not isdigit(s):
                raise ValidationError("There is a character in the phone number.")
    
    uid = models.AutoField(primary_key=True)
    # username = uname
    # password
    # date_joined = time
    sector = models.CharField(max_length=20)
    # email = email
    phone = models.CharField(max_length=11, validators=[validate_phone])
    question1 = models.CharField(max_length=50)
    answer1 = models.CharField(max_length=50)
    question2 = models.CharField(max_length=50)
    answer2 = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username