from django.db import models

# Create your models here.
from users.models import User

STATUS = [
    ('AVAILABLE', 'AVAILABLE'),
    ('BORROWED', 'BORROWED')
]


class Books(models.Model):
    book_name = models.CharField(max_length=200, null=False)
    author_name = models.CharField(max_length=200)
    rate = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='AVAILABLE')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'books'


