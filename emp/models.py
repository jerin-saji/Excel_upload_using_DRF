from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class EmployeeMaster(models.Model):
    user           =  models.OneToOneField(User,unique=True,on_delete=models.SET_NULL,null=True,blank=True,db_index=True)
    employee_code  =  models.CharField(max_length=500,null=True,blank=True)
    fullname       =  models.CharField(max_length=150,null=True,blank=True)
    role           =  models.CharField(max_length=150,null=True,blank=True)
    warehouse      =  models.CharField(max_length=150,null=True,blank=True)
    email          =  models.CharField(max_length=250,null=True,blank=True)
    mobile         =  models.CharField(max_length=50,null=True,blank=True)
    city           =  models.CharField(max_length=150,null=True,blank=True)
    is_active      =  models.BooleanField(default=1)
    inv_owner      =  models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return str(self.fullname)+" - "+str(self.employee_code)


  
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name