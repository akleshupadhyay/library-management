from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class User_Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'user_profile'


