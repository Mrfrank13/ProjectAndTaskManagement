from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Create your models here.
class Project(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='static/ProjectImages')
    description=models.TextField(max_length=50000)
    duration=models.CharField(max_length=100)
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return str(self.name)


class Task(models.Model):
    name=models.CharField(null=False,max_length=100)
    description=models.TextField(null=False,max_length=50000)
    startdate=models.DateField()
    enddate=models.DateField()
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    assignmentFile=models.FileField(upload_to='static/AssignmentFiles',null=True, blank=True)
    assignmentDescription=models.TextField(max_length=50000,null=True,blank=True)
    def __str__(self):
        return str(self.project)
