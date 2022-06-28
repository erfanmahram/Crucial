# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 01:57:18 2022

@author: PC
"""
# -*- coding: utf-8 -*-
#os level command
#Scripts\activate.bat
# cd path
#python manage.py makemigrations
#python manage.py migrate 
#python
#>>>

import os;
os.environ['DJANGO_SETTINGS_MODULE'] = 'project1.settings';
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] =  "true"; # It is needed in an IDE 'Spyder'
import django;
django.setup();

from app1.models import Student;  
from app1.models import Professor; 
from app1.models import Course;
from app1.models import Exam;

from django.db.models import Count


import string 
import random

Exam.objects.all().delete()
Student.objects.all().delete()
Professor.objects.all().delete()
Course.objects.all().delete()

# Assumptions:
s_num = 200 # number of students 
p_num =  10 # number of professors
c_num = 20 # number of courses
e_num = 1000 #number of exam 
 
# We will use pandas to display the queryset in tanular format
import pandas
pandas.options.display.max_rows=30

# Utility function to display querysets
def as_table(values_queryset):
    return pandas.DataFrame(list(values_queryset))               

#Filling Student table
for i in range (0,s_num):
    string_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    string_family = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    s =Student(first_name = string_name, family_name = string_family)
    s.save()
    
#Viewing the table
#student_table = as_table(Student.objects.all().values("first_name", "family_name", "gpa","id")) 
#display(student_table)  
    
    
#Filling Professor table
for i in range (0,p_num):
    string_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    string_family = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    p= Professor(name = string_name+" "+ string_family)
    p.save()
#Filling Course table
## 
prof_id_list=list(Professor.objects.all().values_list('id', flat=True))
prof_id_seletion = random.choices(prof_id_list,k=c_num )


#Filling Exam table
for i in range (0, c_num):
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    c= Course(course_name=name, p_ID = prof_id_seletion[i])    
    c.save()
    
student_id_list=list(Student.objects.all().values_list('id', flat=True))
student_id_seletion = random.choices(student_id_list,k=e_num )

course_id_list=list(Course.objects.all().values_list('id', flat=True))
course_id_seletion = random.choices(course_id_list,k=e_num )

for i in range (0, e_num ):
    e=Exam (s_ID = student_id_seletion[i], c_ID=course_id_seletion[i], grade=round(random.uniform(0, 20), 2) )
    e.save()
          
            
from django.db.models import Avg, F,Max, Window
#from django.db.models.functions import RowNumber
#exams=Exam.objects.annotate(row_number=Window(expression=RowNumber(), partition_by=[F('s_ID'), F('c_ID')], order_by=F('grade').desc(),),)
exams=Exam.objects.annotate(max_grade=Window(expression=Max('grade'), partition_by=[F('s_ID'), F('c_ID')], order_by=F('grade').desc(),),)

#Deleting dublicated records, Keep only the highest grade for each student's exam
#borrowed from https://gist.github.com/victorono/cd9d14b013487b8b22975512225c5b4c
unique_fields = ['s_ID', 'c_ID']
duplicates = (
    exams.all().values(*unique_fields)
    .order_by()
    .annotate(max_id=Max('id'), count_id=Count('id'))
    .filter(count_id__gt=1)
)

for duplicate in duplicates:
    (
        exams.all()
        .filter(**{x: duplicate[x] for x in unique_fields})
        .exclude(id=duplicate['max_id'])
        .delete()
    )

#Calculating the gpa for each student
student_id_list = exams.all().values('s_ID').distinct() # getting the list of the available students IDs in exams queryset
for item in student_id_list:
    sid=item['s_ID']
    x = exams.all().filter (s_ID=sid)
    item=Student.objects.get(id=sid)
    avg=x.all().aggregate(Avg('grade'))
    item.gpa=round(avg['grade__avg'],2)
    item.save()


for x in Student.objects.all():
    print(x.first_name,' ',x.family_name,' ', x.gpa, x.id )
    
#student_table = as_table(Student.objects.all().values("first_name", "family_name", "gpa","id")) 
#display(student_table)     

#Calculating pass percent for each professor
#Eech professor has two courses. Pass_percent is calculated based on two courses 


