from django.db import models

# Create your models here.
# Database ----> Excel Workbook
# Models in Django ----> Table ----> Sheet

class Contact(models.Model):
    Sl_No = models.AutoField(primary_key = True)
    name = models.CharField( max_length=255)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=13)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email