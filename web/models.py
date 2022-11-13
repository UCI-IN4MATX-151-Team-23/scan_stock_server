from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tag = models.TextField(null=False, unique=True)

class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    qrcode = models.TextField(null=False)
    barcode = models.TextField(null=False)
    attrs = models.TextField(default='{}')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tags = models.ManyToManyField(Tag, blank=True)

class ItemTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(null=False)
    description = models.TextField()
    attrs = models.TextField()
