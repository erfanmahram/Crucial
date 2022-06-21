python manage.py makemigrations
python manage.py migrate 

import os;
os.environ['DJANGO_SETTINGS_MODULE'] = 'project1.settings';
import django;
django.setup();

from app1.models import Student;  
from app1.models import Professor; 
from app1.models import Course;
from app1.models import Exam; 
    
s1 =Student(first_name = "AA", family_name = "BB")
s1.save()
s2 =Student(first_name = "CC", family_name = "DD")
s2.save()
s3 =Student(first_name = "EE", family_name = "FF")
s3.save()
 
#p1.student.add(s1,s2,s3)
#p2.student.add(s1,s2)
#p3.student.add(s2,s3)  
    
p1 = Professor(name ="profAA")
p1.save()
p2 = Professor(name ="profBB")
p2.save()
p3 = Professor(name ="profCC")
p3.save()

c1= Course(course_name="course1", prof_name="profBB") 
c1.save()
c2= Course(course_name="course2", prof_name="profAA") 
c2.save()
c3= Course(course_name="course3", prof_name="profCC") 
c3.save()
    
e1= Exam(s_ID=1,c_ID=2,grade=12.5)
e1.save()
e2= Exam(s_ID=1,c_ID=3,grade=17)
e2.save()
    
e3= Exam(s_ID=2,c_ID=1,grade=17)
e3.save()   

e4= Exam(s_ID=2,c_ID=2,grade=19)
e4.save()   

e5= Exam(s_ID=2,c_ID=3,grade=5)
e5.save()   

e6= Exam(s_ID=3,c_ID=1,grade=9)
e6.save()
   
e7= Exam(s_ID=3,c_ID=3,grade=6)
e7.save()   

#Calculating  GPA for each student 
from django.db.models import Avg
for i in range(1,4):
    x = Exam.objects.filter (s_ID=i)
    item=Student.objects.get(id=i)
    avg=x.all().aggregate(Avg('grade'))
    item.gpa=avg['grade__avg']
    item.save()

for x in Student.objects.all():
    print(x.first_name)
    print(x.family_name)
    print(x.gpa)
    
#Calculating pass percent for each profecessor
from django.db.models import Count
from django.db.models import Q
for x in Professor.objects.all():
    y=x.name;
    prof_course= Course.objects.get (prof_name=y)
    course_id =prof_course.id
    total = Exam.objects.filter (c_ID=course_id).all().count()
    student_paased = Exam.objects.filter (Q(c_ID=course_id) & Q(grade__gte=10)).all().count()
    x.pass_percent=student_paased/total*100
    x.save()
    
for x in Professor.objects.all():
    print(x.name)
    print(x.pass_percent)

for y in Course.objects.all():
    print(y.course_name)
    print(y.prof_name)
    
    
    
      
    
   
