from django.db import models

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    gpa = models.FloatField(null=True)
    def __str__(self):
        return self.first_name#,self.family_name , self.gpa
     
class Professor(models.Model):
    name = models.CharField(max_length=100)
    pass_percent = models.FloatField(null=True)
    #student= models.ManyToManyField(Student)

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    prof_name = models.CharField(max_length=100)
    #professor=models.ManyToManyField(Professor)
    #student= models.ManyToManyField(Student)
    
class Exam(models.Model):
   #course = models.OneToOneField(Course,on_delete=models.CASCADE,
   #    primary_key=True)
    s_ID = models.IntegerField()
    c_ID = models.IntegerField()
    grade = models.FloatField()
    
