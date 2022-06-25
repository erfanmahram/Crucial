from django.db import models

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    gpa = models.FloatField(null=True)
    def __str__(self):
        return self.first_name
     
class Professor(models.Model):
    name = models.CharField(max_length=100)
    pass_percent = models.FloatField(null=True)

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    p_ID = models.IntegerField(null=True)
        
class Exam(models.Model):
    s_ID = models.IntegerField()
    c_ID = models.IntegerField()
    grade = models.FloatField()
    

