from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=32)
    birth_date = models.DateField()
    email = models.EmailField()
    tlfn = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    amis = models.ManyToManyField("self", blank=True)
    Faculte = models.ForeignKey('Faculte', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
from django.db import models
from django.contrib.auth.models import User  # Si vous utilisez User ou vos modèles spécifiques




class Faculte(models.Model):
    nom = models.CharField(max_length=32)
    
    def __str__(self):
        return self.nom

class Campus(models.Model):
    nom = models.CharField(max_length=32)
    adresse = models.CharField(max_length=60)
    
    def __str__(self):
        return self.nom

class Job(models.Model):
    titre = models.CharField(max_length=32)
    
    def __str__(self):
        return self.titre

class Cursus(models.Model):
    titre = models.CharField(max_length=32)
    
    def __str__(self):
        return self.titre



class student(Person):
    annee = models.IntegerField()
    cursus = models.ForeignKey('Cursus', on_delete=models.CASCADE)

class Message(models.Model):
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey('student', on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Message from {self.student or self.employee}: {self.contenu}"

class Employee(Person):
    office = models.CharField(max_length=32)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
from .models import student, Employee  # Importez vos modèles personnalisés

class Friend(models.Model):
    user = models.ForeignKey(student, on_delete=models.CASCADE)  # Ou Employee selon vos besoins
    friend_name = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} est ami avec {self.friend_name}"
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('contenu', 'date_publication', 'student', 'employee')
    list_filter = ('date_publication',)
    search_fields = ('contenu', 'student__first_name', 'employee__first_name')
    def __str__(self):
        return self.contenu
