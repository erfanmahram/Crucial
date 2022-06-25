# -*- coding: utf-8 -*-
#os level command
#Scripts\activate.bat
# cd path
python manage.py makemigrations
python manage.py migrate 
python
>>>
import os;
os.environ['DJANGO_SETTINGS_MODULE'] = 'project1.settings';
import django;
django.setup();

from app1.models import Student;  
from app1.models import Professor; 
from app1.models import Course;
from app1.models import Exam;
from django.db.models import Count
from django.db.models import Q 

import string 
import random

#Filling Student table
for i in range (0,200):
    string_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    string_family = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    s =Student(first_name = string_name, family_name = string_family)
    s.save()
#Filling Professor table
for i in range (0,10):
    string_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    string_family = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    p= Professor(name = string_name+" "+ string_family)
    p.save()
#Filling Course table
##each professor have two courses.
for i in range (1,21):
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if (i>10):
        c= Course(course_name=name, p_ID = i-10)
    else:
        c= Course(course_name=name, p_ID = i)
        
    c.save()
    

    
#Filling Exam
#Each student can have up to max_num courses
max_num=4
s_num =  Student.objects.count()
c_num =  Course.objects.count()
course_num_list=[random.randint(1, max_num) for _ in range(s_num)]
#e_num=sum(course_num_list)
sid=1
for i in range (0, s_num ):
    a=course_num_list[i]
    for j in range(0,a):
        e=Exam (s_ID = sid, c_ID=random.randint(1,c_num), grade=round(random.uniform(0, 20), 2) )
        e.save()
        if j== a-1:
            sid=sid+1

#Calculating  GPA for each student 
from django.db.models import Avg
for i in range(1,s_num+1):
    x = Exam.objects.filter (s_ID=i)
    item=Student.objects.get(id=i)
    avg=x.all().aggregate(Avg('grade'))
    item.gpa=round(avg['grade__avg'],2)
    item.save()

for x in Student.objects.all():
    print(x.first_name,' ',x.family_name,' ', x.gpa )
    
    
#Calculating pass percent for each professor
#Eech professor has two courses. Pass_percent is calculated based on two courses 

for p in Professor.objects.all():
    p_courses= Course.objects.filter (p_ID=p.id)#return queryset
    total =0
    student_paased=0
    for c in p_courses.all():
        total = total + Exam.objects.filter (c_ID=c.id).all().count()
        student_paased = student_paased + Exam.objects.filter (Q(c_ID=c.id) & Q(grade__gte=10)).all().count()
    p.pass_percent=round(student_paased/total*100,2)
    p.save()
    
for p in Professor.objects.all():
    print(p.name, " ",p.pass_percent )
    
for c in Course.objects.all():
    print(c.course_name," ", c.p_ID)

for e in Exam.objects.all():
    print(e.s_ID," ", e.c_ID, " " ,e.grade)
  
